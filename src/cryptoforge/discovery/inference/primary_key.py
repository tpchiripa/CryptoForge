"""
=========================================================
CryptoForge Primary Key Inferencer
=========================================================

Attempts to identify candidate primary key columns.

A column is considered a candidate primary key if:

- it contains no missing values
- every value is unique
- it is NOT a continuous numeric measure (price, quantity, amount, ...)

That last condition is what stops columns like `price` from being flagged
as a primary key just because a small sample happens to have no repeated
values. Uniqueness alone is not enough evidence that a column identifies
a row -- a float-typed business measure never should, regardless of how
unique it looks.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import (
    InferenceRegistry,
)

# Column-name hints used only as a fallback when dtype alone can't tell us
# a column is a measure (e.g. an int64 "amount" column with no decimals in
# the current sample). Kept narrow on purpose -- false positives here would
# wrongly disqualify a legitimate key.
_MEASURE_NAME_HINTS = (
    "price", "cost", "amount", "quantity", "qty", "quote_quantity",
    "fee", "total", "revenue", "balance", "weight", "volume",
)


def _is_continuous_measure(series, column_name: str) -> bool:
    """
    True if this column should never be treated as a key candidate,
    regardless of uniqueness.
    """
    name_hit = any(hint in column_name.lower() for hint in _MEASURE_NAME_HINTS)

    if series.dtype.kind == "f":
        non_null = series.dropna()
        has_fraction = (not non_null.empty) and (non_null % 1 != 0).any()
        return bool(has_fraction or name_hit)

    # Non-float columns are only excluded if the name is unambiguous about
    # being a measure (covers int-typed money/quantity columns).
    return name_hit


@InferenceRegistry.register
class PrimaryKeyInferencer(BaseInferencer):
    """
    Detects candidate primary keys.
    """

    def infer(self):

        self.logger.info(
            "Inferring candidate primary keys..."
        )

        candidates = []

        for column in self.df.columns:

            series = self.df[column]

            if series.isna().any():
                continue

            if _is_continuous_measure(series, column):
                self.logger.debug(
                    "Skipping '%s' as primary key candidate: continuous measure.",
                    column,
                )
                continue

            if series.nunique(dropna=False) == len(series):

                candidates.append(column)

        self.logger.info(
            "Detected %s candidate primary keys.",
            len(candidates),
        )

        return {
            "primary_keys": candidates
        }