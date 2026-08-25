-- =========================================================
-- CryptoForge Full Dataset Stats (Spark)
-- =========================================================
-- Appended to the schema for the Spark full-scale profiling job.
-- Links to the same `datasets` table the pandas-based discovery
-- pipeline uses -- one dataset identity, two complementary
-- profiling engines (pandas on a 10K-row sample for fast iterative
-- inference, Spark on the full file for true-scale numbers).
-- =========================================================

CREATE TABLE IF NOT EXISTS full_dataset_stats (
    id                           SERIAL PRIMARY KEY,
    dataset_id                   INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    computed_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),

    total_rows                   BIGINT,
    distinct_rows                BIGINT,
    duplicate_rows                BIGINT,

    min_price                    NUMERIC,
    max_price                    NUMERIC,
    avg_price                    NUMERIC,

    min_quantity                 NUMERIC,
    max_quantity                 NUMERIC,
    avg_quantity                 NUMERIC,

    min_timestamp                TIMESTAMPTZ,
    max_timestamp                TIMESTAMPTZ,

    spark_job_duration_seconds   NUMERIC
);

CREATE INDEX IF NOT EXISTS idx_full_dataset_stats_dataset_id
    ON full_dataset_stats (dataset_id);
