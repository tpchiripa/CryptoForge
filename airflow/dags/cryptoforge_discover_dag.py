"""
=========================================================
CryptoForge Discovery DAG
=========================================================

Runs `python -m cryptoforge discover --to-postgres` on a schedule.

Deliberately a thin wrapper around the already-tested CLI command
rather than re-implementing pipeline calls directly in the DAG --
the CLI's error handling, report writing, and Postgres write-or-warn
behavior are all already verified; the DAG shouldn't duplicate that
logic; a non-zero exit code from the CLI fails the Airflow task
automatically.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# Internal Docker network address -- NOT the host-mapped 5435 port.
# Containers on the forge-network talk to each other by service name
# and the container's own internal port.
POSTGRES_DSN_IN_DOCKER = (
    "postgresql://forge_admin:forge_secure_password@postgres:5432/cryptoforge_dw"
)

default_args = {
    "owner": "cryptoforge",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="cryptoforge_discover",
    description="Runs CryptoForge's dataset discovery pipeline and writes results to Postgres.",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["cryptoforge", "discovery"],
) as dag:

    run_discover = BashOperator(
        task_id="run_discover",
        bash_command=(
            "cd /opt/cryptoforge && "
            "python -m cryptoforge discover --to-postgres --quiet"
        ),
        env={"CRYPTOFORGE_DATABASE_URL": POSTGRES_DSN_IN_DOCKER},
    )