"""
=========================================================
CryptoForge Reporting Framework Test
=========================================================
"""

from pathlib import Path

import cryptoforge.discovery.statistics.basic
import cryptoforge.discovery.statistics.schema
import cryptoforge.discovery.statistics.numeric
import cryptoforge.discovery.statistics.quality
import cryptoforge.discovery.statistics.timestamp

from cryptoforge.discovery.pipeline import DiscoveryPipeline
from cryptoforge.discovery.reporting.writer import ReportWriter
from cryptoforge.discovery.reporting.markdown import (
    MarkdownReportRenderer,
)
from cryptoforge.discovery.reporting.json_report import (
    JsonReportRenderer,
)


def main():

    pipeline = DiscoveryPipeline()

    result = pipeline.run()

    markdown = MarkdownReportRenderer().render(result)

    json_report = JsonReportRenderer().render(result)

    writer = ReportWriter(Path("reports"))

    markdown_path = writer.write(
        "dataset_report.md",
        markdown,
    )

    json_path = writer.write(
        "dataset_report.json",
        json_report,
    )

    print("\nGenerated Reports")
    print("=" * 60)

    print(markdown_path)

    print(json_path)


if __name__ == "__main__":
    main()