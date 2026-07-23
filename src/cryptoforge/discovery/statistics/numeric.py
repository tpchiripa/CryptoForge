"""
Numeric Statistics Calculator

Computes descriptive statistics for every numeric column.
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.discovery.contracts import NumericStatistics
from cryptoforge.discovery.statistics.base import BaseCalculator
from cryptoforge.discovery.statistics.registry import StatisticsRegistry


@StatisticsRegistry.register
class NumericStatisticsCalculator(BaseCalculator):

    def calculate(self) -> NumericStatistics:

        self.logger.info("Calculating numeric statistics...")

        numeric_df = self.df.select_dtypes(include="number")

        summary = {}

        if numeric_df.empty:

            self.logger.warning("No numeric columns detected.")

            return NumericStatistics(summary={})

        for column in numeric_df.columns:

            series = numeric_df[column]

            summary[column] = {

                "count": int(series.count()),

                "minimum": float(series.min()),

                "maximum": float(series.max()),

                "mean": float(series.mean()),

                "median": float(series.median()),

                "std": float(series.std()),

                "variance": float(series.var()),

                "sum": float(series.sum()),

                "unique": int(series.nunique()),

                "q1": float(series.quantile(0.25)),

                "q2": float(series.quantile(0.50)),

                "q3": float(series.quantile(0.75)),

                "skewness": float(series.skew()),

                "kurtosis": float(series.kurt()),

            }

        self.logger.info(
            "Calculated statistics for %d numeric columns.",
            len(summary),
        )

        return NumericStatistics(summary=summary)