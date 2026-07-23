"""
=========================================================
Timestamp Statistics Calculator
=========================================================

Computes profiling information for timestamp columns.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.discovery.contracts import TimestampStatistics
from cryptoforge.discovery.statistics.base import BaseCalculator
from cryptoforge.discovery.statistics.registry import StatisticsRegistry


@StatisticsRegistry.register
class TimestampStatisticsCalculator(BaseCalculator):
    """
    Computes statistics for datetime columns.
    """

    def calculate(self) -> TimestampStatistics:

        self.logger.info("Calculating timestamp statistics...")

        datetime_df = self.df.select_dtypes(include=["datetime"])

        summary = {}

        if datetime_df.empty:

            self.logger.warning("No timestamp columns detected.")

            return TimestampStatistics(summary={})

        for column in datetime_df.columns:

            series = datetime_df[column]

            summary[column] = {

                "minimum": series.min(),

                "maximum": series.max(),

                "missing": int(series.isna().sum()),

                "unique": int(series.nunique()),

                "timezone": str(series.dt.tz)
                if hasattr(series.dt, "tz")
                else None,

                "is_monotonic": bool(
                    series.is_monotonic_increasing
                ),

                "duration_seconds": (
                    (
                        series.max() - series.min()
                    ).total_seconds()
                    if len(series) > 1
                    else 0
                ),
            }

        self.logger.info(
            "Calculated timestamp statistics for %d columns.",
            len(summary),
        )

        return TimestampStatistics(summary=summary)