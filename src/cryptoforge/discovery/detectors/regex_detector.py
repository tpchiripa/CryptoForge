"""
=========================================================
CryptoForge Regex Detector
=========================================================

Reusable detector for validating values using
regular expressions.

Returns a DetectionResult so downstream inferencers
receive confidence scores, matched samples and
statistics.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import re
from typing import Iterable

from cryptoforge.discovery.contracts import DetectionResult


class RegexDetector:
    """
    Applies regex validation against sample values.
    """

    def __init__(self, pattern: str):

        self.pattern = re.compile(pattern)

    def matches(self, value: object) -> bool:
        """
        Validate a single value.
        """

        if value is None:
            return False

        return bool(
            self.pattern.fullmatch(str(value).strip())
        )

    def detect(
        self,
        values: Iterable[object],
    ) -> DetectionResult:
        """
        Execute regex detection.

        Returns
        -------
        DetectionResult
        """

        values = [
            value
            for value in values
            if value is not None
        ]

        if not values:

            return DetectionResult(
                detector="RegexDetector",
                matched=False,
                confidence=0.0,
                evidence=[],
                matched_values=[],
                metadata={},
            )

        matched = [
            value
            for value in values
            if self.matches(value)
        ]

        confidence = len(matched) / len(values)

        return DetectionResult(
            detector="RegexDetector",
            matched=confidence > 0.0,
            confidence=confidence,
            evidence=[str(value) for value in matched[:10]],
            matched_values=[str(value) for value in matched],
            metadata={
                "pattern": self.pattern.pattern,
                "tested_values": len(values),
                "matched_values": len(matched),
            },
        )