"""
=========================================================
CryptoForge Base Reporter
=========================================================

Base class for all report generators.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

from cryptoforge.discovery.contracts import DiscoveryResult


class BaseReporter(ABC):
    """
    Base class for all Discovery reports.
    """

    def __init__(
        self,
        result: DiscoveryResult,
        output_directory: Path,
    ) -> None:

        self.result = result

        self.output_directory = output_directory

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    @abstractmethod
    def generate(self) -> Path:
        """
        Generate the report.

        Returns
        -------
        Path
            Path to generated report.
        """