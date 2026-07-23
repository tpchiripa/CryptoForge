"""
Quality Statistics Calculator

Computes dataset quality metrics.
"""

from __future__ import annotations

from cryptoforge.discovery.contracts import QualityStatistics
from cryptoforge.discovery.statistics.base import BaseCalculator
from cryptoforge.discovery.statistics.registry import StatisticsRegistry


@StatisticsRegistry.register
class QualityStatisticsCalculator(BaseCalculator):

    def calculate(self) -> QualityStatistics:

        self.logger.info("Calculating quality statistics...")

        rows = len(self.df)

        columns = len(self.df.columns)

        total_cells = rows * columns

        missing_values = int(self.df.isna().sum().sum())

        duplicate_rows = int(self.df.duplicated().sum())

        unique_rows = rows - duplicate_rows

        missing_percentage = (
            missing_values / total_cells * 100
            if total_cells
            else 0.0
        )

        duplicate_percentage = (
            duplicate_rows / rows * 100
            if rows
            else 0.0
        )

        completeness_score = 100.0 - missing_percentage

        quality_score = (
            completeness_score -
            duplicate_percentage
        )

        quality_score = max(0.0, round(quality_score, 2))

        self.logger.info(
            "Quality score: %.2f",
            quality_score,
        )

        return QualityStatistics(
            missing_values=missing_values,
            missing_percentage=round(
                missing_percentage,
                2,
            ),
            duplicate_rows=duplicate_rows,
            duplicate_percentage=round(
                duplicate_percentage,
                2,
            ),
            unique_rows=unique_rows,
            completeness_score=round(
                completeness_score,
                2,
            ),
            quality_score=quality_score,
        )