"""
=========================================================
CryptoForge Statistics Engine
=========================================================

Executes every registered statistics calculator.

Importing the statistics package automatically registers
all available calculators with the StatisticsRegistry.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.logger import get_logger

# ---------------------------------------------------------
# IMPORTANT
#
# Importing this package triggers automatic registration
# of every statistics calculator.
# ---------------------------------------------------------
import cryptoforge.discovery.statistics

from cryptoforge.discovery.statistics.registry import (
    StatisticsRegistry,
)

logger = get_logger(__name__)


class StatisticsEngine:
    """
    Executes every registered statistics calculator.
    """

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe

    def calculate(self):
        """
        Execute every registered calculator.

        Returns
        -------
        dict
            Mapping of calculator name -> calculator result.
        """

        logger.info("Executing Statistics Engine...")

        results = {}

        for calculator in StatisticsRegistry.calculators():

            logger.info(
                "Running %s...",
                calculator.__name__,
            )

            instance = calculator(self.df)

            results[calculator.__name__] = (
                instance.calculate()
            )

        logger.info(
            "Statistics Engine completed successfully."
        )

        return results
