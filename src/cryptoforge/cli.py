"""
=========================================================
CryptoForge CLI
=========================================================

Command-line entry point for running the discovery pipeline.

Usage
-----
    python -m cryptoforge discover
    python -m cryptoforge discover --output-dir reports
    python -m cryptoforge discover --to-postgres
    python -m cryptoforge --help

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import argparse
import sys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cryptoforge",
        description="CryptoForge data discovery and metadata inference engine.",
    )

    subparsers = parser.add_subparsers(dest="command")

    discover_parser = subparsers.add_parser(
        "discover",
        help="Run the discovery pipeline against the dataset in data/raw/ and write a report.",
    )
    discover_parser.add_argument(
        "--output-dir",
        default="reports",
        help="Directory to write dataset_report.json/.md into (default: reports)",
    )
    discover_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress the summary printed to stdout (reports are still written).",
    )
    discover_parser.add_argument(
        "--to-postgres",
        action="store_true",
        help=(
            "Also write the discovery result into the Postgres metadata "
            "warehouse (see postgres/init.sql). Requires Postgres to be "
            "running (docker compose up -d postgres) and psycopg2-binary "
            "installed. Connection defaults to the docker-compose "
            "credentials on localhost:5435; override with the "
            "CRYPTOFORGE_DATABASE_URL environment variable."
        ),
    )

    return parser


def _run_discover(args: argparse.Namespace) -> int:
    # Imported here, not at module level, so `python -m cryptoforge --help`
    # stays fast and doesn't require a dataset/config to exist just to
    # print usage text.
    from cryptoforge.discovery.pipeline import DiscoveryPipeline
    from cryptoforge.discovery.report import DiscoveryReportWriter

    pipeline = DiscoveryPipeline()

    try:
        result = pipeline.run()
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Discovery pipeline failed: {exc}", file=sys.stderr)
        return 1

    writer = DiscoveryReportWriter(result, output_dir=args.output_dir)
    json_path = writer.write_json()
    md_path = writer.write_markdown()

    postgres_run_id = None
    postgres_error = None
    if args.to_postgres:
        # A Postgres failure should never take down a discovery run that
        # otherwise succeeded and already has JSON/Markdown reports
        # written -- report it clearly, but exit 0, not crash.
        from cryptoforge.discovery.postgres_writer import PostgresWriter

        try:
            postgres_run_id = PostgresWriter().write(result)
        except Exception as exc:  # noqa: BLE001
            postgres_error = str(exc)

    if not args.quiet:
        inf = result.inference
        print()
        print("Discovery complete.")
        print(f"  JSON report:     {json_path}")
        print(f"  Markdown report: {md_path}")

        if args.to_postgres:
            if postgres_run_id is not None:
                print(f"  Postgres:        written (discovery_runs.id = {postgres_run_id})")
            else:
                print(f"  Postgres:        FAILED -- {postgres_error}", file=sys.stderr)

        print()
        print(f"  Primary keys:     {inf.primary_keys}")
        print(f"  Identifiers:      {inf.identifiers}")
        print(f"  Name columns:     {inf.name_columns}")
        print(f"  Company columns:  {inf.company_columns}")
        print(f"  Country columns:  {inf.country_columns}")
        print(f"  Currency columns: {inf.currency_columns}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "discover":
        return _run_discover(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
