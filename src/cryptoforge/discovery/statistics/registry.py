"""
=========================================================
CryptoForge Statistics Registry
=========================================================

Maintains a registry of all statistics calculators.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from typing import Type

from cryptoforge.discovery.statistics.base import BaseCalculator


class StatisticsRegistry:
    """
    Registry for all statistics calculators.
    """

    _calculators: list[Type[BaseCalculator]] = []

    @classmethod
    def register(cls, calculator: Type[BaseCalculator]) -> None:

        if calculator not in cls._calculators:
            cls._calculators.append(calculator)

    @classmethod
    def calculators(cls):

        return cls._calculators.copy()

    @classmethod
    def clear(cls):

        cls._calculators.clear()

    @classmethod
    def count(cls):

        return len(cls._calculators)