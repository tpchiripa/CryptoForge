"""
=========================================================
CryptoForge Categorical Inferencer
=========================================================

Infers categorical columns.

A categorical column is one having relatively few unique
values compared to the total number of rows.

Typical examples

    country
    gender
    status
    side
    exchange

Boolean columns are treated as categorical.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class CategoricalInferencer(BaseInferencer):
    """
    Detect categorical columns.
    """

    CARDINALITY_THRESHOLD = 0.05

    def infer(self) -> dict:
        """
        Detect categorical columns.
        """

        self.logger.info(
            "Inferring categorical columns..."
        )

        categorical_columns = []

        total_rows = len(self.df)

        for column in self.df.columns:

            series = self.df[column]

            # -------------------------------------------------
            # Ignore datetime columns
            # -------------------------------------------------

            if pd.api.types.is_datetime64_any_dtype(series):
                continue

            # -------------------------------------------------
            # Ignore constant columns
            # -------------------------------------------------

            if series.nunique(dropna=False) <= 1:
                continue

            # -------------------------------------------------
            # Boolean columns are categorical
            # -------------------------------------------------

            if pd.api.types.is_bool_dtype(series):
                categorical_columns.append(column)
                continue

            # -------------------------------------------------
            # Low-cardinality columns
            # -------------------------------------------------

            cardinality = (
                series.nunique(dropna=False)
                / total_rows
            )

            if cardinality <= self.CARDINALITY_THRESHOLD:
                categorical_columns.append(column)

        self.logger.info(
            "Detected %s categorical columns.",
            len(categorical_columns),
        )

        return {
            "categorical_columns": categorical_columns
        }