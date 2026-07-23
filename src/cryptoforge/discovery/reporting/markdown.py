"""
=========================================================
CryptoForge Markdown Report Renderer
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.contracts import DiscoveryResult


class MarkdownReportRenderer:
    """
    Generates a Markdown report.
    """

    def render(
        self,
        result: DiscoveryResult,
    ) -> str:

        lines = []

        lines.append("# CryptoForge Dataset Report")
        lines.append("")

        lines.append("## Dataset")
        lines.append("")
        lines.append(f"- ZIP File: **{result.dataset.zip_file}**")
        lines.append(f"- CSV File: **{result.dataset.csv_file}**")
        lines.append(
            f"- Compression: **{result.dataset.compression_ratio_percent}%**"
        )

        lines.append("")
        lines.append("## Basic Statistics")
        lines.append("")

        lines.append(f"- Sample Rows: {result.basic.sample_rows:,}")
        lines.append(f"- Columns: {result.basic.column_count}")
        lines.append(f"- Missing Values: {result.basic.missing_values}")
        lines.append(f"- Duplicate Rows: {result.basic.duplicate_rows}")

        lines.append("")
        lines.append("## Schema")
        lines.append("")

        for column, dtype in result.schema.dtypes.items():
            lines.append(f"- {column}: {dtype}")

        lines.append("")
        lines.append("## Quality")

        lines.append("")
        lines.append(
            f"- Quality Score: {result.quality.quality_score:.2f}"
        )

        return "\n".join(lines)