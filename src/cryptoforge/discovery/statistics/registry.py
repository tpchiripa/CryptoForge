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
    def register(
        cls,
        calculator: Type[BaseCalculator],
    ) -> Type[BaseCalculator]:
        """
        Register a calculator and return it so the decorator
        does not replace the class with None.
        """

        if calculator not in cls._calculators:
            cls._calculators.append(calculator)

        return calculator

    @classmethod
    def calculators(cls) -> list[Type[BaseCalculator]]:
        return cls._calculators.copy()

    @classmethod
    def clear(cls) -> None:
        cls._calculators.clear()

    @classmethod
    def count(cls) -> int:
        return len(cls._calculators)
