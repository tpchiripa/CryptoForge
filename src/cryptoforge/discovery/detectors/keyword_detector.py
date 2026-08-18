"""
=========================================================
CryptoForge Keyword Detector
=========================================================

Reusable detector for keyword-based metadata inference.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from typing import Iterable


class KeywordDetector:
    """
    Detects columns whose names contain one or more keywords.

    Example
    -------
    detector = KeywordDetector({"email", "mail"})

    detector.matches("customer_email")
    True

    detector.matches("trade_id")
    False
    """

    def __init__(self, keywords: Iterable[str]) -> None:

        self.keywords = {
            keyword.lower().strip()
            for keyword in keywords
        }

    def matches(self, column_name: str) -> bool:
        """
        Returns True if any keyword exists
        inside the supplied column name.
        """

        column = column_name.lower()

        return any(
            keyword in column
            for keyword in self.keywords
        )

    def detect(self, columns: Iterable[str]) -> list[str]:
        """
        Detect matching columns.
        """

        return [
            column
            for column in columns
            if self.matches(column)
        ]