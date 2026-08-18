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
from cryptoforge.discovery.inference.semantic_base import (
    BaseSemanticInferencer,
)
from cryptoforge.discovery.detectors.dictionary_detector import (
    DictionaryDetector,
)
from cryptoforge.discovery.resources.paths import dataset_path
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
            dataset_path("first_names.csv")
        )
        self.surnames = DictionaryDetector(
            dataset_path("surnames.csv")
        )
    def evaluate(
        self,
        column: str,
        samples: list[str],
    ) -> float:
        """
        Evaluate how confidently the sampled values
        represent personal names.
        """
        first_result = self.first_names.detect(samples)
        surname_result = self.surnames.detect(samples)
        return max(
            first_result.confidence,
            surname_result.confidence,
        )
