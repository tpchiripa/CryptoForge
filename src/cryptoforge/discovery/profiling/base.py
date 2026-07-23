"""
=========================================================
CryptoForge Profiling Base Class
=========================================================

Defines the abstract base class for all profiling
calculators.

Every profiler receives a pandas DataFrame and returns
a profiling contract.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from cryptoforge.logger import get_logger


class BaseProfiler(ABC):
    """
    Base class for all profiling calculators.
    """

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe

        self.logger = get_logger(self.__class__.__name__)

        self.logger.info(
            "Initialized with %d rows and %d columns.",
            len(self.df),
            len(self.df.columns),
        )

    @abstractmethod
    def profile(self):
        """
        Execute the profiler.

        Returns
        -------
        Domain contract describing the profiling result.
        """
        raise NotImplementedError