"""
=========================================================
Identifier Inferencer
=========================================================

Infers columns that appear to represent identifiers.

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
class IdentifierInferencer(BaseInferencer):
    """
    Detect identifier columns.

    Examples
    --------
    trade_id
    customer_id
    order_id
    uuid
    hash
    wallet_address
    """

    NAME_PATTERNS = (
        "id",
        "uuid",
        "guid",
        "key",
        "code",
        "number",
        "reference",
        "ref",
        "hash",
        "token",
    )

    UNIQUENESS_THRESHOLD = 0.90

    def __init__(self, dataframe: pd.DataFrame):

        super().__init__(dataframe)

        self.logger = get_logger(self.__class__.__name__)

    def infer(self) -> dict:

        self.logger.info(
            "Inferring identifier columns..."
        )

        identifiers = []

        total_rows = len(self.df)

        for column in self.df.columns:

            series = self.df[column]

            name = column.lower()

            # -----------------------------------------
            # Skip obvious non-identifiers
            # -----------------------------------------

            if pd.api.types.is_bool_dtype(series):
                continue

            if pd.api.types.is_datetime64_any_dtype(series):
                continue

            if not (
                pd.api.types.is_numeric_dtype(series)
                or pd.api.types.is_string_dtype(series)
                or series.dtype == object
            ):
                continue

            uniqueness = series.nunique(dropna=True) / total_rows

            has_identifier_name = any(
                pattern in name
                for pattern in self.NAME_PATTERNS
            )

            if has_identifier_name or uniqueness >= self.UNIQUENESS_THRESHOLD:
                identifiers.append(column)

        self.logger.info(
            "Detected %d identifier columns.",
            len(identifiers),
        )

        return {
            "identifiers": identifiers
        }