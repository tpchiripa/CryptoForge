"""
=========================================================
CryptoForge Schema Statistics Calculator
=========================================================

Builds schema metadata from a DataFrame.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.contracts import SchemaInfo
from cryptoforge.discovery.statistics.base import BaseCalculator


class SchemaStatisticsCalculator(BaseCalculator):
    """
    Calculates schema information.
    """

    def calculate(self) -> SchemaInfo:

        self.logger.info("Calculating schema information...")

        columns = list(self.df.columns)

        dtypes = {
            column: str(dtype)
            for column, dtype in self.df.dtypes.items()
        }

        self.logger.info(
            "Detected %s columns.",
            len(columns),
        )

        return SchemaInfo(
            columns=columns,
            dtypes=dtypes,
        )
from cryptoforge.discovery.statistics.registry import StatisticsRegistry

StatisticsRegistry.register(SchemaStatisticsCalculator)