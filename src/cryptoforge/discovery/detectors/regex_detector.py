"""
=========================================================
CryptoForge Regex Detector
=========================================================

Reusable detector for validating values using
regular expressions.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import re
from typing import Iterable


class RegexDetector:
    """
    Applies regex validation against sample values.

    Useful for:

    - Email
    - Phone
    - Barcode
    - UUID
    - VAT Number
    - Passport
    - Tax Number
    """

    def __init__(self, pattern: str):

        self.pattern = re.compile(pattern)

    def matches(self, value: object) -> bool:
        """
        Validate one value.
        """

        if value is None:
            return False

        return bool(
            self.pattern.fullmatch(str(value).strip())
        )

    def score(
        self,
        values: Iterable[object],
    ) -> float:
        """
        Percentage of values matching the regex.

        Returns
        -------
        float
            Score between 0 and 1.
        """

        values = list(values)

        if not values:
            return 0.0

        matches = sum(
            self.matches(value)
            for value in values
        )

        return matches / len(values)