"""
=========================================================
CryptoForge Sample Detector
=========================================================

Extract representative samples from dataframe columns.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd


class SampleDetector:
    """
    Returns clean sample values from a dataframe column.

    Used by:

    • EmailInferencer
    • PhoneInferencer
    • BarcodeInferencer
    • SKUInferencer
    • NameInferencer
    """

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe

    def sample(
        self,
        column: str,
        size: int = 100,
    ) -> list:

        if column not in self.df.columns:
            return []

        values = (
            self.df[column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        values = values[
            values != ""
        ]

        return (
            values
            .head(size)
            .tolist()
        )