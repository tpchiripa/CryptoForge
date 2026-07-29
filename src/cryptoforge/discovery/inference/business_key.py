"""
=========================================================
CryptoForge Business Key Inferencer
=========================================================

Attempts to identify candidate business keys.

A business key differs from a primary key because it
has business meaning rather than being purely technical.

Current implementation is heuristic-based.

Future versions will incorporate metadata catalog,
domain rules and cross-dataset validation.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class BusinessKeyInferencer(BaseInferencer):
    """
    Detect candidate business keys.
    """

    def infer(self) -> dict:

        self.logger.info(
            "Inferring business keys..."
        )

        business_keys = []

        for column in self.df.columns:

            series = self.df[column]

            name = column.lower()

            if any(
                keyword in name
                for keyword in (
                    "code",
                    "symbol",
                    "account",
                    "customer",
                    "client",
                    "product",
                    "invoice",
                    "order",
                    "reference",
                    "number",
                )
            ):

                if (
                    not series.isna().any()
                    and series.nunique() == len(series)
                ):
                    business_keys.append(column)

        self.logger.info(
            "Detected %d business keys.",
            len(business_keys),
        )

        return {
            "business_keys": business_keys
        }