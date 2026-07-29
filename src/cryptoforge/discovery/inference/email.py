"""
=========================================================
CryptoForge Email Inferencer
=========================================================

Infers email address columns.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import re

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class EmailInferencer(BaseInferencer):
    """
    Detect email columns.
    """

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    NAME_HINTS = {
        "email",
        "email_address",
        "mail",
    }

    def infer(self):

        self.logger.info(
            "Inferring email columns..."
        )

        email_columns = []

        for column in self.df.columns:

            lower = column.lower()

            if lower in self.NAME_HINTS:

                email_columns.append(column)
                continue

            series = self.df[column].dropna().astype(str)

            if len(series) == 0:
                continue

            matches = series.str.match(
                self.EMAIL_PATTERN
            )

            if matches.mean() > 0.80:
                email_columns.append(column)

        self.logger.info(
            "Detected %d email columns.",
            len(email_columns),
        )

        return {
            "email_columns": email_columns
        }