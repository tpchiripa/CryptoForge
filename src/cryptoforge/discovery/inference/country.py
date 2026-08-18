"""
=========================================================
CryptoForge Country Inferencer
=========================================================

Infers country columns using the CryptoForge
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
class CountryInferencer(BaseSemanticInferencer):
    """
    Detect country columns.
    """

    KEYWORDS = {
        "country",
        "nation",
        "nationality",
        "citizenship",
        "origin",
        "country_name",
    }

    RESULT_KEY = "country_columns"

    def __init__(self, df):

        super().__init__(df)

        self.country_dictionary = DictionaryDetector(
            "src/cryptoforge/discovery/resources/datasets/countries.csv"
        )

    def evaluate(
        self,
        column,
        samples,
    ):

        return self.country_dictionary.score(samples)