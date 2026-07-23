"""
=========================================================
CryptoForge JSON Reporter
=========================================================
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from cryptoforge.discovery.reporting.base import BaseReporter


class JsonReporter(BaseReporter):

    REPORT_NAME = "Dataset_Profile.json"

    def generate(self) -> Path:

        output = self.output_directory / self.REPORT_NAME

        output.write_text(
            json.dumps(
                asdict(self.result),
                indent=4,
                default=str,
            ),
            encoding="utf-8",
        )

        return output