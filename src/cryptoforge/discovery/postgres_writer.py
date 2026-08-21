"""
=========================================================
CryptoForge Postgres Writer
=========================================================

Writes a DiscoveryResult into the Postgres metadata warehouse
(see postgres/init.sql for the schema).

Connection is configured via the CRYPTOFORGE_DATABASE_URL environment
variable, falling back to the default docker-compose credentials for
local development:
    postgresql://forge_admin:forge_secure_password@localhost:5435/cryptoforge_dw

Design note: rather than hardcoding every InferenceResult field name
(primary_keys, identifiers, currency_columns, semantic_types, ...),
_write_inference_findings() iterates dataclasses.fields(inference)
generically. List-typed fields become one (category, column, NULL)
row per column; dict-typed fields become one (category, column, value)
row per entry. This means adding a new inferencer/category later
requires zero changes here -- it's picked up automatically.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import dataclasses
import os

from cryptoforge.logger import get_logger

logger = get_logger(__name__)

DEFAULT_DSN = (
    "postgresql://forge_admin:forge_secure_password@localhost:5435/cryptoforge_dw"
)


class PostgresWriter:
    """
    Usage:
        writer = PostgresWriter()
        run_id = writer.write(discovery_result)
    """

    def __init__(self, dsn: str | None = None):
        self.dsn = dsn or os.environ.get("CRYPTOFORGE_DATABASE_URL", DEFAULT_DSN)

    def _connect(self):
        # Imported here, not at module level, so importing this module
        # doesn't require psycopg2 to be installed unless you actually
        # use Postgres persistence.
        import psycopg2
        return psycopg2.connect(self.dsn)

    def write(self, result) -> int:
        """
        Persists a DiscoveryResult. Returns the discovery_runs.id of
        the newly created run.
        """
        conn = self._connect()
        try:
            with conn:
                with conn.cursor() as cur:
                    dataset_id = self._upsert_dataset(cur, result.dataset)
                    run_id = self._insert_run(cur, dataset_id, result)
                    self._write_column_profiles(cur, run_id, result.column_profiles)
                    self._write_inference_findings(cur, run_id, result.inference)
            logger.info("Wrote discovery run %s to Postgres.", run_id)
            return run_id
        finally:
            conn.close()

    # =====================================================
    # Internal helpers
    # =====================================================

    @staticmethod
    def _upsert_dataset(cur, dataset) -> int:
        cur.execute(
            """
            INSERT INTO datasets (zip_file, csv_file)
            VALUES (%s, %s)
            ON CONFLICT (zip_file, csv_file)
            DO UPDATE SET zip_file = EXCLUDED.zip_file
            RETURNING id
            """,
            (
                getattr(dataset, "zip_file", None),
                getattr(dataset, "csv_file", None),
            ),
        )
        return cur.fetchone()[0]

    @staticmethod
    def _insert_run(cur, dataset_id: int, result) -> int:
        dataset = result.dataset
        basic = getattr(result, "basic", None)
        quality = getattr(result, "quality", None)

        cur.execute(
            """
            INSERT INTO discovery_runs (
                dataset_id,
                zip_size_bytes, csv_size_bytes, compression_ratio_percent,
                sample_rows, column_count, missing_values, duplicate_rows,
                completeness_score, quality_score,
                missing_percentage, duplicate_percentage
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING id
            """,
            (
                dataset_id,
                getattr(dataset, "zip_size_bytes", None),
                getattr(dataset, "csv_size_bytes", None),
                getattr(dataset, "compression_ratio_percent", None),
                getattr(basic, "sample_rows", None),
                getattr(basic, "column_count", None),
                getattr(basic, "missing_values", None),
                getattr(basic, "duplicate_rows", None),
                getattr(quality, "completeness_score", None),
                getattr(quality, "quality_score", None),
                getattr(quality, "missing_percentage", None),
                getattr(quality, "duplicate_percentage", None),
            ),
        )
        return cur.fetchone()[0]

    @staticmethod
    def _write_column_profiles(cur, run_id: int, profiles) -> None:
        if not profiles:
            return
        for p in profiles:
            cur.execute(
                """
                INSERT INTO column_profiles (
                    run_id, column_name, dtype, nullable,
                    missing_values, missing_percentage,
                    unique_values, cardinality
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (run_id, column_name) DO NOTHING
                """,
                (
                    run_id,
                    getattr(p, "name", None),
                    getattr(p, "dtype", None),
                    getattr(p, "nullable", None),
                    getattr(p, "missing_values", None),
                    getattr(p, "missing_percentage", None),
                    getattr(p, "unique_values", None),
                    getattr(p, "cardinality", None),
                ),
            )

    @staticmethod
    def _write_inference_findings(cur, run_id: int, inference) -> None:
        if inference is None:
            return

        rows: list[tuple] = []

        for f in dataclasses.fields(inference):
            value = getattr(inference, f.name)
            category = f.name

            if isinstance(value, dict):
                for column, mapped_value in value.items():
                    rows.append((run_id, category, str(column), str(mapped_value)))
            elif isinstance(value, (list, tuple, set)):
                for column in value:
                    rows.append((run_id, category, str(column), None))
            # scalar/other field types on InferenceResult are skipped --
            # this table only models per-column findings.

        for row in rows:
            cur.execute(
                """
                INSERT INTO inference_findings (run_id, category, column_name, value)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (run_id, category, column_name) DO UPDATE
                    SET value = EXCLUDED.value
                """,
                row,
            )