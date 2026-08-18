"""
=========================================================
Duplicate Inferencer
=========================================================

Detects columns that are exact duplicates of another column in the
same dataset (i.e. redundant, could be dropped without losing
information).

Previous behavior (bug): used `series.duplicated().sum() > 0`, which
counts internally-repeated VALUES within a single column -- that's a
low-cardinality signal (almost any column except a fully-unique one
like an ID will trigger it), not "this column duplicates another
column." On a real dataset this flagged nearly every column. Fixed
here to compare whole columns against each other and only flag a
column when it is genuinely identical, value-for-value, to an earlier
one.

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
    Detect duplicate columns (columns identical to another column).
    """

    name = "DuplicateInferencer"

    def infer(self) -> dict:

        self.logger.info("Inferring duplicate columns...")

        duplicate_columns = []
        duplicate_of = {}

        seen: dict[tuple, str] = {}

        for column in self.df.columns:

            # Tuple of the column's values is a simple, exact,
            # order-sensitive fingerprint -- two columns only produce
            # the same key if every value matches in every row.
            key = tuple(self.df[column].tolist())

            if key in seen:
                duplicate_columns.append(column)
                duplicate_of[column] = seen[key]
                self.logger.debug(
                    "'%s' is an exact duplicate of '%s'",
                    column,
                    seen[key],
                )
            else:
                seen[key] = column

        self.logger.info(
            "Detected %d duplicate columns.",
            len(duplicate_columns),
        )

        return {
            "duplicate_columns": duplicate_columns,
            "duplicate_of": duplicate_of,
        }
