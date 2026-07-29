"""
=========================================================
CryptoForge Semantic Type Inferencer
=========================================================

Attempts to classify the business meaning of columns.

Examples

price
quantity
timestamp
currency
email
phone
country
city
percentage
identifier

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import re

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class SemanticTypeInferencer(BaseInferencer):
    """
    Infer business semantic types.
    """

    RULES = {

        "price": [
            "price",
            "cost",
            "amount",
            "value",
        ],

        "quantity": [
            "qty",
            "quantity",
            "volume",
        ],

        "timestamp": [
            "timestamp",
            "time",
            "date",
            "datetime",
        ],

        "currency": [
            "currency",
            "fx",
        ],

        "email": [
            "email",
            "mail",
        ],

        "phone": [
            "phone",
            "mobile",
            "cell",
        ],

        "country": [
            "country",
            "nation",
        ],

        "city": [
            "city",
            "town",
        ],

        "percentage": [
            "percent",
            "percentage",
            "rate",
        ],

        "identifier": [
            "id",
            "identifier",
            "key",
        ],
    }

    def infer(self):

        self.logger.info(
            "Inferring semantic column types..."
        )

        semantic_types = {}

        for column in self.df.columns:

            lower = column.lower()

            detected = "unknown"

            for semantic_type, patterns in self.RULES.items():

                if any(
                    re.search(pattern, lower)
                    for pattern in patterns
                ):
                    detected = semantic_type
                    break

            semantic_types[column] = detected

        self.logger.info(
            "Detected semantic types for %d columns.",
            len(semantic_types),
        )

        return {
            "semantic_types": semantic_types
        }