"""
=========================================================
CryptoForge Company Inferencer
=========================================================
Infers company columns using the CryptoForge
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
class CompanyInferencer(BaseSemanticInferencer):
    """
    Detect company columns.
    """
    KEYWORDS = {
        "company",
        "organisation",
        "organization",
        "employer",
        "vendor",
        "supplier",
        "customer_company",
        "business",
        "corporation",
        "firm",
    }
    RESULT_KEY = "company_columns"
    def __init__(self, df):
        super().__init__(df)
        self.detector = DictionaryDetector(
            dataset_path("companies.csv")
        )
    def evaluate(
        self,
        column: str,
        samples: list[str],
    ) -> float:
        """
        Evaluate how confidently the sampled values
        represent company names.
        """
        result = self.detector.detect(samples)
        return result.confidence
