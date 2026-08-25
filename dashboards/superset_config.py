"""
=========================================================
CryptoForge Superset Configuration
=========================================================

Minimal config -- points Superset at its own metadata database
(superset_db, a separate logical database inside the same Postgres
instance CryptoForge and Airflow already use -- same pattern as
airflow_db, no extra container needed).

Author:
    Tichaona Peter Chiripa
=========================================================
"""

import os

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://forge_admin:forge_secure_password@postgres:5432/superset_db"

# Required since Superset 3.x -- no longer has an insecure default.
# Set via docker-compose environment; falls back here only if that's
# somehow missing.
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "changeme-for-local-dev-only")