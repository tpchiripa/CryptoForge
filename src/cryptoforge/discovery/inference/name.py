"""
=========================================================
CryptoForge Name Inferencer
=========================================================

Infers personal name columns using the CryptoForge
Knowledge Base.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.registry import register
from cryptoforge.discovery.inference.semantic_base import BaseSemanticInferencer

from cryptoforge.discovery.detectors.dictionary_detector import DictionaryDetector


@register
class NameInferencer(BaseSemanticInferencer):
    """
    Detect columns containing personal names.
    """

    KEYWORDS = {
        "name",
        "first_name",
        "firstname",
        "given_name",
        "forename",
        "last_name",
        "lastname",
        "surname",
        "family_name",
        "customer_name",
        "employee_name",
        "full_name",
    }

    RESULT_KEY = "name_columns"

    def __init__(self, df):

        super().__init__(df)

        self.first_names = DictionaryDetector(
            "src/cryptoforge/discovery/resources/datasets/first_names.csv"
        )

        self.surnames = DictionaryDetector(
            "src/cryptoforge/discovery/resources/datasets/surnames.csv"
        )

    def evaluate(
        self,
        column,
        samples,
    ):

        first_score = self.first_names.score(samples)

        surname_score = self.surnames.score(samples)

        return max(
            first_score,
            surname_score,
        )