"""
=========================================================
CryptoForge JSON Report Renderer
=========================================================
"""

from __future__ import annotations

import json
from dataclasses import asdict

from cryptoforge.discovery.contracts import DiscoveryResult


class JsonReportRenderer:
    """
    Converts DiscoveryResult into JSON.
    """

    def render(
        self,
        result: DiscoveryResult,
    ) -> str:

        return json.dumps(
            asdict(result),
            indent=4,
            default=str,
        )