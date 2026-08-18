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
from cryptoforge.discovery.inference.semantic_base import BaseSemanticInferencer

from cryptoforge.discovery.detectors.dictionary_detector import DictionaryDetector


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

        self.company_dictionary = DictionaryDetector(
            "src/cryptoforge/discovery/resources/datasets/companies.csv"
        )

    def evaluate(
        self,
        column,
        samples,
    ):

        return self.company_dictionary.score(samples)