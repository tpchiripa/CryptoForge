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

# Same measure-name fallback used in primary_key.py. Kept in sync
# deliberately -- if you add a hint to one, add it to the other, or move
# both to a shared module (see note at bottom of file).
_MEASURE_NAME_HINTS = (
    "price", "cost", "amount", "quantity", "qty", "quote_quantity",
    "fee", "total", "revenue", "balance", "weight", "volume",
)


def _is_continuous_measure(series: pd.Series, column_name: str) -> bool:
    name_hit = any(hint in column_name.lower() for hint in _MEASURE_NAME_HINTS)

    if series.dtype.kind == "f":
        non_null = series.dropna()
        has_fraction = (not non_null.empty) and (non_null % 1 != 0).any()
        return bool(has_fraction or name_hit)

    return name_hit


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

            if _is_continuous_measure(series, column):
                self.logger.debug(
                    "Skipping '%s' as identifier candidate: continuous measure.",
                    column,
                )
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

# NOTE: _MEASURE_NAME_HINTS and _is_continuous_measure are now duplicated
# in both primary_key.py and identifier.py. Worth moving to a shared
# module (e.g. inference/_measures.py) once we're past the immediate fix
# so the two lists can't quietly drift apart.