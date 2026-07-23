"""
=========================================================
CryptoForge Primary Key Inferencer
=========================================================

Attempts to identify candidate primary key columns.

A column is considered a candidate primary key if:

- it contains no missing values
- every value is unique

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import (
    InferenceRegistry,
)


@InferenceRegistry.register
class PrimaryKeyInferencer(BaseInferencer):
    """
    Detects candidate primary keys.
    """

    def infer(self):

        self.logger.info(
            "Inferring candidate primary keys..."
        )

        candidates = []

        for column in self.df.columns:

            series = self.df[column]

            if series.isna().any():
                continue

            if series.nunique(dropna=False) == len(series):

                candidates.append(column)

        self.logger.info(
            "Detected %s candidate primary keys.",
            len(candidates),
        )

        return {
            "primary_keys": candidates
        }