# =========================================================
# CryptoForge Spark Master Image
# =========================================================
# Extends the official Spark image with psycopg2 installed, so the
# driver process (which runs inside this container when a job is
# spark-submit'd here) can write its final aggregate results directly
# into Postgres after the distributed computation collects back to
# the driver.
#
# Workers do NOT need this -- they only execute serialized Spark
# tasks (reading Parquet, running aggregations); the Postgres write
# happens once, in driver-side Python code, after results are small
# enough to collect. Workers keep using the stock apache/spark image
# directly in docker-compose.yml -- no rebuild needed for them.
# =========================================================

FROM apache/spark:4.0.3

USER root
RUN pip install --no-cache-dir psycopg2-binary
USER spark
