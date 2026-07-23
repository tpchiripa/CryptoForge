"""
=========================================================
CryptoForge High Cardinality Inferencer
=========================================================

Detect columns with many unique values.

A high-cardinality column has a large proportion of
distinct values relative to the dataset size.

Examples
--------
trade_id
timestamp
price

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class HighCardinalityInferencer(BaseInferencer):
    """
    Detect high-cardinality columns.
    """

    # configurable threshold
    THRESHOLD = 0.90

    def infer(self) -> dict:

        self.logger.info(
            "Inferring high-cardinality columns..."
        )

        high_cardinality = []

        total_rows = len(self.df)

        for column in self.df.columns:

            if total_rows == 0:
                continue

            unique_ratio = (
                self.df[column]
                .nunique(dropna=False)
                / total_rows
            )

            if unique_ratio >= self.THRESHOLD:

                high_cardinality.append(column)

        self.logger.info(
            "Detected %s high-cardinality columns.",
            len(high_cardinality),
        )

        return {
            "high_cardinality_columns": high_cardinality
        }