"""
One-off manual test: run the real discovery pipeline against your real
dataset, then write the result into Postgres. Prints the resulting
discovery_runs.id so you can go query it directly and confirm the data
actually landed correctly.

Run from the repo root:
    python test_postgres_writer.py

Requires Postgres to already be up (docker compose up -d postgres) and
psycopg2-binary installed (pip install psycopg2-binary).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from cryptoforge.discovery.pipeline import DiscoveryPipeline
from cryptoforge.discovery.postgres_writer import PostgresWriter


def main():
    print("Running discovery pipeline against real dataset...")
    result = DiscoveryPipeline().run()

    print("Writing result to Postgres...")
    writer = PostgresWriter()
    run_id = writer.write(result)

    print()
    print(f"SUCCESS. discovery_runs.id = {run_id}")
    print()
    print("Verify with:")
    print(f'  docker exec -it cryptoforge-postgres psql -U forge_admin -d cryptoforge_dw -c "SELECT * FROM discovery_runs WHERE id = {run_id};"')
    print(f'  docker exec -it cryptoforge-postgres psql -U forge_admin -d cryptoforge_dw -c "SELECT * FROM column_profiles WHERE run_id = {run_id};"')
    print(f'  docker exec -it cryptoforge-postgres psql -U forge_admin -d cryptoforge_dw -c "SELECT category, column_name, value FROM inference_findings WHERE run_id = {run_id} ORDER BY category;"')


if __name__ == "__main__":
    main()
