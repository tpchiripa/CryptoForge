"""
=========================================================
CryptoForge Inference Base
=========================================================

Base class for all metadata inference components.

Every inferencer derives from this class and implements
the infer() method.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from cryptoforge.logger import get_logger


class BaseInferencer(ABC):
    """
    Base class for all metadata inferencers.

    Every inferencer receives the sampled dataframe
    and returns one or more metadata discoveries.
    """

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe

        self.logger = get_logger(self.__class__.__name__)

        self.logger.info(
            "Initialized with %s rows and %s columns.",
            len(self.df),
            len(self.df.columns),
        )

    @abstractmethod
    def infer(self):
        """
        Execute metadata inference.

        Returns
        -------
        Any
            Metadata discovered by the inferencer.
        """
        raise NotImplementedError