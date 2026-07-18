"""
Basic Statistics Calculator
"""

from cryptoforge.discovery.contracts import BasicStatistics
from cryptoforge.discovery.statistics.base import BaseCalculator


class BasicStatisticsCalculator(BaseCalculator):

    def calculate(self) -> BasicStatistics:

        self.logger.info(
            "Calculating basic statistics..."
        )

        return BasicStatistics(
            sample_rows=self.row_count,
            column_count=self.column_count,
            missing_values=self.missing_values,
            duplicate_rows=self.duplicate_rows,
            memory_bytes=self.memory_usage,
        )
from cryptoforge.discovery.statistics.registry import StatisticsRegistry

StatisticsRegistry.register(BasicStatisticsCalculator)