-- =========================================================
-- CryptoForge Metadata Warehouse Schema
-- =========================================================
-- Runs automatically on first Postgres container start (mounted into
-- /docker-entrypoint-initdb.d/ -- see docker-compose.yml).
--
-- NOTE: Postgres only runs init scripts when the data directory is
-- EMPTY. If you've already run `docker compose up` once before and
-- have an existing postgres_data volume, this script will NOT re-run
-- automatically. To force a fresh init:
--     docker compose down -v
--     docker compose up -d postgres
-- (the -v flag deletes the volume -- only do this if you don't need
-- to keep existing data in it)
-- =========================================================

-- One row per distinct source file CryptoForge has ever profiled.
-- Re-running discovery against the same file again does NOT create a
-- new dataset row -- it creates a new discovery_runs row against the
-- same dataset, so history accumulates per file over time.
CREATE TABLE IF NOT EXISTS datasets (
    id              SERIAL PRIMARY KEY,
    zip_file        TEXT NOT NULL,
    csv_file        TEXT NOT NULL,
    first_seen_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (zip_file, csv_file)
);

-- One row per pipeline execution ("discover" run) against a dataset.
CREATE TABLE IF NOT EXISTS discovery_runs (
    id                          SERIAL PRIMARY KEY,
    dataset_id                  INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    run_at                      TIMESTAMPTZ NOT NULL DEFAULT now(),

    zip_size_bytes              BIGINT,
    csv_size_bytes              BIGINT,
    compression_ratio_percent   NUMERIC,

    sample_rows                 INTEGER,
    column_count                INTEGER,
    missing_values              INTEGER,
    duplicate_rows              INTEGER,

    completeness_score          NUMERIC,
    quality_score                NUMERIC,
    missing_percentage          NUMERIC,
    duplicate_percentage        NUMERIC
);

CREATE INDEX IF NOT EXISTS idx_discovery_runs_dataset_id
    ON discovery_runs (dataset_id);

CREATE INDEX IF NOT EXISTS idx_discovery_runs_run_at
    ON discovery_runs (run_at);

-- One row per column, per run -- the ColumnProfile contract.
CREATE TABLE IF NOT EXISTS column_profiles (
    id                  SERIAL PRIMARY KEY,
    run_id              INTEGER NOT NULL REFERENCES discovery_runs(id) ON DELETE CASCADE,
    column_name         TEXT NOT NULL,
    dtype               TEXT,
    nullable            BOOLEAN,
    missing_values      INTEGER,
    missing_percentage  NUMERIC,
    unique_values       INTEGER,
    cardinality         NUMERIC,

    UNIQUE (run_id, column_name)
);

CREATE INDEX IF NOT EXISTS idx_column_profiles_run_id
    ON column_profiles (run_id);

-- One row per (category, column) inference result, per run. Every
-- category on InferenceResult -- primary_keys, identifiers,
-- currency_columns, semantic_types, everything -- funnels into this
-- one generic table as (category, column_name, value) triples. Plain
-- list categories (e.g. primary_keys) get value = NULL; dict
-- categories (e.g. currency_columns, semantic_types) get value = the
-- mapped string. This means new inference categories added later
-- don't require a schema migration -- the writer code that populates
-- this table iterates InferenceResult's fields generically.
CREATE TABLE IF NOT EXISTS inference_findings (
    id              SERIAL PRIMARY KEY,
    run_id          INTEGER NOT NULL REFERENCES discovery_runs(id) ON DELETE CASCADE,
    category        TEXT NOT NULL,
    column_name     TEXT NOT NULL,
    value           TEXT,

    UNIQUE (run_id, category, column_name)
);

CREATE INDEX IF NOT EXISTS idx_inference_findings_run_id
    ON inference_findings (run_id);

CREATE INDEX IF NOT EXISTS idx_inference_findings_category
    ON inference_findings (category);
