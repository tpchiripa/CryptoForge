"""
=========================================================
CryptoForge Statistics Package
=========================================================

Automatically imports and registers all available
statistics calculators.

Importing this package ensures every calculator
registers itself with the StatisticsRegistry.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from cryptoforge.discovery.statistics.basic import BasicStatisticsCalculator
from cryptoforge.discovery.statistics.schema import SchemaStatisticsCalculator
from cryptoforge.discovery.statistics.numeric import NumericStatisticsCalculator
from cryptoforge.discovery.statistics.quality import QualityStatisticsCalculator
from cryptoforge.discovery.statistics.timestamp import TimestampStatisticsCalculator

__all__ = [
    "BasicStatisticsCalculator",
    "SchemaStatisticsCalculator",
    "NumericStatisticsCalculator",
    "QualityStatisticsCalculator",
    "TimestampStatisticsCalculator",
]