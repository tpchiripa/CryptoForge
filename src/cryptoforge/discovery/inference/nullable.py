"""
=========================================================
CryptoForge Nullable Inferencer
=========================================================

Infers columns that contain missing (NULL) values.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class NullableInferencer(BaseInferencer):
    """
    Detect nullable columns.
    """

    def infer(self) -> dict:
        """
        Detect columns containing NULL values.

        Returns
        -------
        dict
        """

        self.logger.info(
            "Inferring nullable columns..."
        )

        nullable_columns = []

        for column in self.df.columns:

            if self.df[column].isna().any():

                nullable_columns.append(column)

        self.logger.info(
            "Detected %s nullable columns.",
            len(nullable_columns),
        )

        return {
            "nullable_columns": nullable_columns
        }