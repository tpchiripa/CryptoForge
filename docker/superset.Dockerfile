# =========================================================
# CryptoForge Superset Image
# =========================================================
# The official Superset image doesn't ship a Postgres driver by
# default -- same gap we hit with Airflow and Spark. Adds
# psycopg2-binary into Superset's own venv (documented pattern for
# extending this image).
# =========================================================

FROM apache/superset:latest

USER root
RUN /usr/local/bin/pip install --no-cache-dir --target /app/.venv/lib/python3.10/site-packages psycopg2-binary
USER superset