"""
=========================================================
CryptoForge Dictionary Detector
=========================================================

Supports dictionary matching from either:

1. Python sets
2. CSV knowledge bases

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from pathlib import Path

from cryptoforge.discovery.detectors.knowledge_cache import KnowledgeCache


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

    def matches(self, value):
        """
        Returns True if the supplied value exists
        inside the dictionary.
        """

        if value is None:
            return False

        value = str(value).strip().lower()

        return value in self.dictionary

    def score(self, samples):
        """
        Returns the fraction of sample values that
        exist inside the dictionary.
        """

        if not samples:
            return 0.0

        matches = sum(
            self.matches(value)
            for value in samples
        )

        return matches / len(samples)