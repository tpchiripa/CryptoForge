"""
=========================================================
CryptoForge Currency Inferencer
=========================================================

Attempts to infer monetary columns.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class CurrencyInferencer(BaseInferencer):
    """
    Detect monetary columns.
    """

    KEYWORDS = {
        "price",
        "amount",
        "cost",
        "total",
        "subtotal",
        "balance",
        "salary",
        "income",
        "expense",
        "revenue",
        "profit",
        "payment",
        "tax",
        "vat",
        "fee",
        "charge",
        "quote_quantity",
    }

    def infer(self):

        self.logger.info(
            "Inferring currency columns..."
        )

        currency_columns = {}

        for column in self.df.columns:

            lower = column.lower()

            if any(keyword in lower for keyword in self.KEYWORDS):

                currency_columns[column] = "UNKNOWN"

        self.logger.info(
            "Detected %d monetary columns.",
            len(currency_columns),
        )

        return {
            "currency_columns": currency_columns
        }