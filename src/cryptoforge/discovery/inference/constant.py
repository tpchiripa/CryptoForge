"""
=========================================================
CryptoForge Constant Inferencer
=========================================================

Detects columns containing a single unique value.

Examples
--------
is_best_match

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class ConstantInferencer(BaseInferencer):
    """
    Detect constant columns.
    """

    def infer(self) -> dict:
        """
        Detect columns whose values never change.

        Returns
        -------
        dict
        """

        self.logger.info(
            "Inferring constant columns..."
        )

        constant_columns = []

        for column in self.df.columns:

            series = self.df[column]

            # Ignore nullable columns
            if series.isna().any():
                continue

            if series.nunique(dropna=False) == 1:
                constant_columns.append(column)

        self.logger.info(
            "Detected %s constant columns.",
            len(constant_columns),
        )

        return {
            "constant_columns": constant_columns
        }