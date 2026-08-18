"""
=========================================================
CryptoForge PII Inferencer
=========================================================

Infers personally identifiable information (PII)
using CryptoForge Knowledge Base.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.registry import register
from cryptoforge.discovery.inference.semantic_base import BaseSemanticInferencer

from cryptoforge.discovery.detectors.dictionary_detector import DictionaryDetector


@register
class PIIInferencer(BaseSemanticInferencer):
    """
    Detect PII columns while excluding business identifiers.
    """

    KEYWORDS = {
        "passport",
        "passport_number",
        "identity",
        "identity_number",
        "national_id",
        "driver_license",
        "drivers_license",
        "tax_number",
        "tin",
        "ssn",
        "credit_card",
        "bank_account",
        "customer_id",
        "employee_id",
        "user_id",
    }

    RESULT_KEY = "pii_columns"

    def __init__(self, df):

        super().__init__(df)

        self.pii_dictionary = DictionaryDetector(
            "src/cryptoforge/discovery/resources/datasets/pii/pii_identifiers.csv"
        )

        self.non_pii_dictionary = DictionaryDetector(
            "src/cryptoforge/discovery/resources/datasets/pii/non_pii_identifiers.csv"
        )

    def evaluate(
        self,
        column,
        samples,
    ):

        # Business identifiers should NEVER be classified as PII
        if self.non_pii_dictionary.matches(column):
            return 0.0

        # Genuine PII identifier names receive high confidence
        if self.pii_dictionary.matches(column):
            return 1.0

        return 0.0