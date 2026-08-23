# =========================================================
# CryptoForge Airflow Image
# =========================================================
# Extends the official Airflow image with CryptoForge itself and its
# dependencies installed, so DAGs can actually import and run the
# discovery pipeline rather than just shelling out blind.
#
# Build context is the repo root (see docker-compose.yml), so this
# Dockerfile can COPY the whole project in.
# =========================================================

FROM apache/airflow:2.10.4-python3.11

USER root

# Nothing extra needed at the OS level for CryptoForge's pure-Python
# dependencies (pandas/psycopg2-binary ship as wheels) -- keeping this
# minimal rather than installing build-essential etc. we don't need.

USER airflow

# Install CryptoForge's own dependencies into Airflow's Python
# environment. Using --no-deps on the editable install would be
# tempting to keep things minimal, but the project's real dependency
# list (pandas, pyyaml, psycopg2-binary) needs to be present for the
# pipeline to actually run -- so install requirements first, then the
# package itself in editable mode.
COPY --chown=airflow:root pyproject.toml /opt/cryptoforge/pyproject.toml
COPY --chown=airflow:root src /opt/cryptoforge/src

RUN pip install --no-cache-dir /opt/cryptoforge

# The DAG imports `cryptoforge.*` directly (not via subprocess), so
# make sure the src layout is importable regardless of how Airflow
# resolves the editable install's .pth file.
ENV PYTHONPATH="/opt/cryptoforge/src:${PYTHONPATH}"