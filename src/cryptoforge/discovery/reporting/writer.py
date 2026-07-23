"""
=========================================================
CryptoForge Report Writer
=========================================================

Responsible for writing generated reports to disk.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from pathlib import Path


class ReportWriter:
    """
    Writes report content to disk.
    """

    def __init__(self, output_directory: Path):

        self.output_directory = output_directory
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write(
        self,
        filename: str,
        content: str,
    ) -> Path:
        """
        Persist report to disk.
        """

        path = self.output_directory / filename

        path.write_text(
            content,
            encoding="utf-8",
        )

        return path