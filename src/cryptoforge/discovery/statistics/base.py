"""
=========================================================
CryptoForge Base Calculator
=========================================================

Provides shared functionality for every Discovery
statistics calculator.

Responsibilities
----------------
- Validate DataFrame
- Store DataFrame
- Configure logging
- Provide reusable helper methods

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from cryptoforge.logger import get_logger


class BaseCalculator(ABC):
    """
    Base class for all Discovery calculators.
    """

    def __init__(self, dataframe: pd.DataFrame):

        if dataframe is None:
            raise ValueError("DataFrame cannot be None.")

        if dataframe.empty:
            raise ValueError("DataFrame cannot be empty.")

        self.df = dataframe

        self.logger = get_logger(self.__class__.__name__)

        self.logger.info(
            "Initialized with %s rows and %s columns.",
            len(self.df),
            len(self.df.columns),
        )

    @property
    def row_count(self) -> int:
        return len(self.df)

    @property
    def column_count(self) -> int:
        return len(self.df.columns)

    @property
    def memory_usage(self) -> int:
        return int(
            self.df.memory_usage(deep=True).sum()
        )

    @property
    def missing_values(self) -> int:
        return int(
            self.df.isna().sum().sum()
        )

    @property
    def duplicate_rows(self) -> int:
        return int(
            self.df.duplicated().sum()
        )

    def numeric_columns(self):
        return self.df.select_dtypes(
            include="number"
        )

    @abstractmethod
    def calculate(self):
        """
        Every calculator must implement calculate().
        """
        pass