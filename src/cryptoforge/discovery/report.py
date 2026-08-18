"""
=========================================================
CryptoForge Discovery Report Writer
=========================================================

Writes a DiscoveryResult out as JSON (complete, machine-readable)
and Markdown (human-readable summary).

The JSON writer uses dataclasses.asdict(), which introspects the
live dataclass fields at runtime -- it will always capture every
field on DiscoveryResult/InferenceResult/etc regardless of exact
naming, so it can't silently drop data due to a naming mismatch.

The Markdown writer accesses fields defensively via getattr() with
fallbacks, so a missing/renamed field produces "(unavailable)" in
the report rather than crashing the whole pipeline run over
formatting -- a report bug should never be able to take down a
successful discovery run.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import dataclasses
import json
from datetime import datetime, timezone
from pathlib import Path

from cryptoforge.logger import get_logger

logger = get_logger(__name__)


def _json_default(obj):
    if isinstance(obj, (set, frozenset)):
        return sorted(obj)
    if isinstance(obj, Path):
        return str(obj)
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    return str(obj)


def _g(obj, name, default="(unavailable)"):
    """Safe getattr for report formatting -- never raises."""
    try:
        value = getattr(obj, name)
        return value if value is not None else default
    except Exception:
        return default


class DiscoveryReportWriter:
    """
    Writes DiscoveryResult objects to reports/dataset_report.json
    and reports/dataset_report.md.
    """

    def __init__(self, result, output_dir: str = "reports"):
        self.result = result
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # =====================================================
    # JSON
    # =====================================================

    def write_json(self, filename: str = "dataset_report.json") -> Path:
        path = self.output_dir / filename
        try:
            data = dataclasses.asdict(self.result)
        except Exception as exc:
            logger.warning("Falling back to str() for JSON report: %s", exc)
            data = {"error": f"Could not fully serialize result: {exc}"}
        data["_generated_at"] = datetime.now(timezone.utc).isoformat()
        with path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, default=_json_default)
        logger.info("Wrote JSON report to %s", path)
        return path

    # =====================================================
    # Markdown
    # =====================================================

    def write_markdown(self, filename: str = "dataset_report.md") -> Path:
        path = self.output_dir / filename
        r = self.result
        lines: list[str] = []

        lines.append("# CryptoForge Discovery Report")
        lines.append("")
        lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
        lines.append("")

        dataset = _g(r, "dataset", None)
        if dataset is not None:
            lines.append("## Dataset")
            lines.append(f"- ZIP file: `{_g(dataset, 'zip_file')}`")
            lines.append(f"- CSV file: `{_g(dataset, 'csv_file')}`")
            lines.append(f"- ZIP size: {_g(dataset, 'zip_size_bytes')} bytes")
            lines.append(f"- CSV size: {_g(dataset, 'csv_size_bytes')} bytes")
            lines.append(f"- Compression ratio: {_g(dataset, 'compression_ratio_percent')}%")
            lines.append("")

        basic = _g(r, "basic", None)
        if basic is not None:
            lines.append("## Basic Statistics")
            lines.append(f"- Sample rows: {_g(basic, 'sample_rows')}")
            lines.append(f"- Columns: {_g(basic, 'column_count')}")
            lines.append(f"- Missing values: {_g(basic, 'missing_values')}")
            lines.append(f"- Duplicate rows: {_g(basic, 'duplicate_rows')}")
            lines.append("")

        quality = _g(r, "quality", None)
        if quality is not None:
            lines.append("## Data Quality")
            lines.append(f"- Completeness score: {_g(quality, 'completeness_score')}")
            lines.append(f"- Quality score: {_g(quality, 'quality_score')}")
            lines.append(f"- Missing percentage: {_g(quality, 'missing_percentage')}%")
            lines.append(f"- Duplicate percentage: {_g(quality, 'duplicate_percentage')}%")
            lines.append("")

        inf = _g(r, "inference", None)
        if inf is not None:
            lines.append("## Inference Results")
            lines.append("")

            sections = [
                ("Primary Keys", "primary_keys"),
                ("Identifiers", "identifiers"),
                ("Business Keys", "business_keys"),
                ("Foreign Keys", "foreign_keys"),
                ("Categorical Columns", "categorical_columns"),
                ("Monotonic Columns", "monotonic_columns"),
                ("Constant Columns", "constant_columns"),
                ("Nullable Columns", "nullable_columns"),
                ("High Cardinality Columns", "high_cardinality_columns"),
                ("Duplicate Columns", "duplicate_columns"),
                ("PII Columns", "pii_columns"),
                ("Email Columns", "email_columns"),
                ("Phone Columns", "phone_columns"),
                ("Address Columns", "address_columns"),
                ("Country Columns", "country_columns"),
                ("Name Columns", "name_columns"),
                ("Company Columns", "company_columns"),
                ("Product Columns", "product_columns"),
                ("SKU Columns", "sku_columns"),
                ("Barcode Columns", "barcode_columns"),
            ]

            for title, attr in sections:
                values = _g(inf, attr, [])
                lines.append(f"### {title}")
                if values and values != "(unavailable)":
                    for v in values:
                        lines.append(f"- {v}")
                else:
                    lines.append("- (none detected)")
                lines.append("")

            for title, attr in [
                ("Semantic Types", "semantic_types"),
                ("Currency Columns", "currency_columns"),
                ("Units", "units"),
            ]:
                mapping = _g(inf, attr, {})
                if mapping and mapping != "(unavailable)":
                    lines.append(f"### {title}")
                    for col, val in mapping.items():
                        lines.append(f"- `{col}` -> {val}")
                    lines.append("")

        profiles = _g(r, "column_profiles", [])
        if profiles and profiles != "(unavailable)":
            lines.append("## Column Profiles")
            lines.append("")
            lines.append("| Column | Dtype | Nullable | Missing % | Unique | Cardinality |")
            lines.append("|---|---|---|---|---|---|")
            for p in profiles:
                lines.append(
                    f"| {_g(p, 'name')} | {_g(p, 'dtype')} | {_g(p, 'nullable')} | "
                    f"{_g(p, 'missing_percentage')} | {_g(p, 'unique_values')} | "
                    f"{_g(p, 'cardinality')} |"
                )
            lines.append("")

        path.write_text("\n".join(lines), encoding="utf-8")
        logger.info("Wrote Markdown report to %s", path)
        return path
