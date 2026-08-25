"""
=========================================================
CryptoForge Spark Job: Convert & Profile Full Dataset
=========================================================

Two stages, run as one job:

  1. Extract the raw CSV from the Binance trade-data ZIP (Spark can't
     read directly from inside a .zip archive) and convert the FULL
     dataset -- not a 10,000-row pandas sample -- to Parquet. This is
     the real "at scale" step: pandas can't reasonably hold this file
     in memory; Spark processes it distributed across the cluster.

  2. Read the Parquet back and compute true full-dataset statistics
     (real row count, real min/max/avg price, real duplicate count
     across every row) and write them into Postgres as a new
     full_dataset_stats row, linked to the same `datasets` table the
     pandas-based discovery pipeline already writes to -- one dataset
     identity, two complementary profiling engines.

Run via spark-submit from inside the spark-master container:
    docker exec -it cryptoforge-spark-master \\
        /opt/spark/bin/spark-submit \\
        --master spark://spark-master:7077 \\
        /opt/spark/jobs/convert_and_profile.py

CANNOT BE TEST-RUN in the environment this was written in (no pyspark
available, no live Spark cluster to submit to) -- written carefully
against documented Spark APIs, but this is the first genuinely
untested piece of code handed over this whole project. Expect to do
real first-run debugging here, the same honest expectation set before
starting this work.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import os
import time
import zipfile
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct, avg, min as spark_min, max as spark_max, expr

# =====================================================
# Paths (container-internal -- see docker-compose.yml volume mounts)
# =====================================================

DATA_ROOT = Path("/opt/spark/data")
RAW_DIR = DATA_ROOT / "raw"
EXTRACTED_DIR = DATA_ROOT / "raw" / "extracted"
SILVER_DIR = DATA_ROOT / "silver"

# Same column order/names as cryptoforge.discovery.inspector.DatasetInspector
# .BINANCE_COLUMNS, so results are directly comparable to the pandas-based
# discovery pipeline's output for the same dataset.
BINANCE_COLUMNS = [
    "trade_id",
    "price",
    "quantity",
    "quote_quantity",
    "timestamp",
    "is_buyer_maker",
    "is_best_match",
]

# Internal Docker network address -- this job runs INSIDE the cluster,
# not on the host, so it uses the container-to-container address, not
# the host-mapped 5435 port (same distinction as the Airflow DAG).
DEFAULT_DSN_IN_DOCKER = (
    "postgresql://forge_admin:forge_secure_password@postgres:5432/cryptoforge_dw"
)


# =====================================================
# Stage 1: Extract + Convert to Parquet
# =====================================================

def locate_dataset_zip() -> Path:
    zip_files = sorted(RAW_DIR.glob("*.zip"))
    if not zip_files:
        raise FileNotFoundError(f"No ZIP files found in {RAW_DIR}")
    return zip_files[0]


def extract_csv(zip_path: Path) -> Path:
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as archive:
        csv_names = [n for n in archive.namelist() if n.endswith(".csv")]
        if not csv_names:
            raise RuntimeError(f"No CSV found inside {zip_path}")
        csv_name = csv_names[0]

        extracted_path = EXTRACTED_DIR / csv_name
        if extracted_path.exists():
            print(f"Already extracted: {extracted_path}")
            return extracted_path

        print(f"Extracting {csv_name} from {zip_path} ...")
        archive.extract(csv_name, path=EXTRACTED_DIR)
        print(f"Extracted to {extracted_path}")
        return extracted_path


def convert_to_parquet(spark: SparkSession, csv_path: Path) -> Path:
    output_path = SILVER_DIR / (csv_path.stem + "_parquet")

    if output_path.exists():
        print(f"Parquet already exists at {output_path}, skipping conversion.")
        return output_path

    print(f"Reading full CSV from {csv_path} (this is the FULL file, not a sample) ...")

    # Read everything as string first -- avoids Spark's CSV type-inference
    # edge cases on messy source data; cast explicitly afterward instead.
    raw = (
        spark.read
        .option("header", "false")
        .csv(str(csv_path))
        .toDF(*BINANCE_COLUMNS)
    )

    typed = raw.select(
        col("trade_id").cast("long"),
        col("price").cast("double"),
        col("quantity").cast("double"),
        col("quote_quantity").cast("double"),
        # Raw value is microseconds since epoch, matching
        # pandas' `pd.to_datetime(..., unit="us")` in inspector.py.
        expr("timestamp_micros(cast(timestamp as long))").alias("timestamp"),
        (col("is_buyer_maker") == "True").alias("is_buyer_maker"),
        (col("is_best_match") == "True").alias("is_best_match"),
    )

    print(f"Writing full dataset as Parquet to {output_path} ...")
    typed.write.mode("overwrite").parquet(str(output_path))
    print("Parquet write complete.")

    return output_path


# =====================================================
# Stage 2: Compute full-dataset statistics
# =====================================================

def compute_full_stats(spark: SparkSession, parquet_path: Path) -> dict:
    print(f"Reading Parquet from {parquet_path} for full-scale stats ...")
    df = spark.read.parquet(str(parquet_path))

    total_rows = df.count()
    distinct_rows = df.distinct().count()

    agg = df.agg(
        spark_min("price").alias("min_price"),
        spark_max("price").alias("max_price"),
        avg("price").alias("avg_price"),
        spark_min("quantity").alias("min_quantity"),
        spark_max("quantity").alias("max_quantity"),
        avg("quantity").alias("avg_quantity"),
        spark_min("timestamp").alias("min_timestamp"),
        spark_max("timestamp").alias("max_timestamp"),
    ).collect()[0]

    stats = {
        "total_rows": total_rows,
        "distinct_rows": distinct_rows,
        "duplicate_rows": total_rows - distinct_rows,
        "min_price": agg["min_price"],
        "max_price": agg["max_price"],
        "avg_price": agg["avg_price"],
        "min_quantity": agg["min_quantity"],
        "max_quantity": agg["max_quantity"],
        "avg_quantity": agg["avg_quantity"],
        "min_timestamp": agg["min_timestamp"],
        "max_timestamp": agg["max_timestamp"],
    }

    print("Full-dataset stats computed:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    return stats


# =====================================================
# Write results to Postgres
# =====================================================

def write_stats_to_postgres(zip_path: Path, csv_path: Path, stats: dict, duration_seconds: float) -> None:
    import psycopg2

    dsn = os.environ.get("CRYPTOFORGE_DATABASE_URL", DEFAULT_DSN_IN_DOCKER)
    conn = psycopg2.connect(dsn)
    try:
        with conn:
            with conn.cursor() as cur:
                # Same upsert pattern as PostgresWriter._upsert_dataset --
                # links this run to the same dataset identity the pandas
                # pipeline already uses, rather than creating a duplicate.
                cur.execute(
                    """
                    INSERT INTO datasets (zip_file, csv_file)
                    VALUES (%s, %s)
                    ON CONFLICT (zip_file, csv_file)
                    DO UPDATE SET zip_file = EXCLUDED.zip_file
                    RETURNING id
                    """,
                    (zip_path.name, csv_path.name),
                )
                dataset_id = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO full_dataset_stats (
                        dataset_id, total_rows, distinct_rows, duplicate_rows,
                        min_price, max_price, avg_price,
                        min_quantity, max_quantity, avg_quantity,
                        min_timestamp, max_timestamp,
                        spark_job_duration_seconds
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        dataset_id,
                        stats["total_rows"],
                        stats["distinct_rows"],
                        stats["duplicate_rows"],
                        stats["min_price"],
                        stats["max_price"],
                        stats["avg_price"],
                        stats["min_quantity"],
                        stats["max_quantity"],
                        stats["avg_quantity"],
                        stats["min_timestamp"],
                        stats["max_timestamp"],
                        duration_seconds,
                    ),
                )
        print("Wrote full_dataset_stats row to Postgres.")
    finally:
        conn.close()


# =====================================================
# Main
# =====================================================

def main() -> None:
    start = time.time()

    spark = (
        SparkSession.builder
        .appName("CryptoForge-ConvertAndProfile")
        .getOrCreate()
    )

    try:
        zip_path = locate_dataset_zip()
        csv_path = extract_csv(zip_path)
        parquet_path = convert_to_parquet(spark, csv_path)
        stats = compute_full_stats(spark, parquet_path)

        duration = time.time() - start
        write_stats_to_postgres(zip_path, csv_path, stats, duration)

        print(f"\nJob completed in {duration:.1f} seconds.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
