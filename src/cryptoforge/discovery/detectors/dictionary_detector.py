"""
=========================================================
CryptoForge Dictionary Detector
=========================================================

Supports dictionary matching from either:

1. Python sets
2. CSV knowledge bases

Returns a DetectionResult so every detector exposes
the same interface to inferencers.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from cryptoforge.discovery.contracts import DetectionResult
from cryptoforge.discovery.detectors.knowledge_cache import (
    KnowledgeCache,
)


class DictionaryDetector:
    """
    Detect values using a dictionary.

    The dictionary may be supplied either as:

    - a Python iterable
    - a CSV knowledge base
    """

    def __init__(self, dictionary):

        if isinstance(dictionary, (str, Path)):
            self.dictionary = KnowledgeCache.load(dictionary)
        else:
            self.dictionary = {
                str(value).strip().lower()
                for value in dictionary
            }

    def matches(
        self,
        value: object,
    ) -> bool:
        """
        Returns True if the supplied value exists
        inside the dictionary.
        """

        if value is None:
            return False

        value = str(value).strip().lower()

        return value in self.dictionary

    def detect(
        self,
        values: Iterable[object],
    ) -> DetectionResult:
        """
        Execute dictionary detection.
        """

        values = [
            value
            for value in values
            if value is not None
        ]

        if not values:

            return DetectionResult(
                detector="DictionaryDetector",
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
            detector="DictionaryDetector",
            matched=confidence > 0.0,
            confidence=confidence,
            evidence=[str(value) for value in matched[:10]],
            matched_values=[str(value) for value in matched],
            metadata={
                "dictionary_size": len(self.dictionary),
                "tested_values": len(values),
                "matched_values": len(matched),
            },
        )