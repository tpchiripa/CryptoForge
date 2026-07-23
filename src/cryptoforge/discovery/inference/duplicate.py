"""
=========================================================
Duplicate Inferencer
=========================================================

Detects columns that contain duplicate values.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class DuplicateInferencer(BaseInferencer):
    """
    Detect duplicate columns.
    """

    name = "DuplicateInferencer"

    def infer(self) -> dict:

        self.logger.info("Inferring duplicate columns...")

        duplicate_columns = []

        for column in self.df.columns:

            duplicate_count = self.df[column].duplicated().sum()

            if duplicate_count > 0:

                duplicate_columns.append(column)

        self.logger.info(
            "Detected %d duplicate columns.",
            len(duplicate_columns),
        )

        return {
            "duplicate_columns": duplicate_columns,
        }