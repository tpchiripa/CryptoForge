"""
=========================================================
CryptoForge Foreign Key Inferencer
=========================================================

Infers potential foreign key columns.

Current implementation is heuristic-based and only
inspects the current dataframe.

Future versions will compare against multiple datasets
stored in the Metadata Catalog.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.logger import get_logger

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class ForeignKeyInferencer(BaseInferencer):
    """
    Detect possible foreign keys.
    """

    def infer(self) -> dict:

        logger = get_logger(self.__class__.__name__)

        logger.info("Inferring foreign keys...")

        foreign_keys = []

        # Placeholder implementation.
        #
        # True FK inference requires comparing this
        # dataframe against other datasets.

        for column in self.df.columns:

            series = self.df[column]

            if (
                pd.api.types.is_integer_dtype(series)
                and not series.is_unique
                and series.nunique() > 1
            ):
                foreign_keys.append(column)

        logger.info(
            "Detected %d possible foreign keys.",
            len(foreign_keys),
        )

        return {
            "foreign_keys": foreign_keys
        }