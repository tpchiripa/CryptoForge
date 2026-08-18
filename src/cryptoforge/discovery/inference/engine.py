"""
=========================================================
CryptoForge Inference Engine
=========================================================

Executes every registered metadata inferencer.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd
import cryptoforge.discovery.inference.autoload

from cryptoforge.logger import get_logger
from cryptoforge.discovery.inference.registry import (
    InferenceRegistry,
)

logger = get_logger(__name__)


class InferenceEngine:
    """
    Executes all registered metadata inferencers.
    """

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe

    def infer(self):

        logger.info("Executing Inference Engine...")

        results = {}

        for inferencer in InferenceRegistry.inferencers():

            logger.info(
                "Running %s...",
                inferencer.__name__,
            )

            instance = inferencer(self.df)

            results[inferencer.__name__] = (
                instance.infer()
            )

        logger.info(
            "Inference Engine completed successfully."
        )

        return results