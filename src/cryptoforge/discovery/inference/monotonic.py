"""
=========================================================
CryptoForge Monotonic Inferencer
=========================================================

Infers columns whose values are monotonically ordered.

A monotonic column is one that is either:

    • monotonically increasing
    • monotonically decreasing

Examples
--------
trade_id      ✓
timestamp     ✓

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class MonotonicInferencer(BaseInferencer):
    """
    Detect monotonic columns.
    """

    def infer(self) -> dict:
        """
        Detect monotonic columns.

        Returns
        -------
        dict
        """

        self.logger.info(
            "Inferring monotonic columns..."
        )

        monotonic_columns = []

        for column in self.df.columns:

            series = self.df[column]

            # Skip columns containing null values
            if series.isna().any():
                continue

            try:

                if (
                    series.is_monotonic_increasing
                    or series.is_monotonic_decreasing
                ):
                    monotonic_columns.append(column)

            except Exception:
                continue

        self.logger.info(
            "Detected %s monotonic columns.",
            len(monotonic_columns),
        )

        return {
            "monotonic_columns": monotonic_columns
        }