"""
=========================================================
CryptoForge Product Inferencer
=========================================================

Infers product columns using the CryptoForge
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
class ProductInferencer(BaseSemanticInferencer):
    """
    Detect product columns.
    """

    KEYWORDS = {
        "product",
        "item",
        "goods",
        "material",
        "commodity",
        "asset",
        "inventory",
        "stock_item",
        "product_name",
        "description",
    }

    RESULT_KEY = "product_columns"

    def __init__(self, df):

        super().__init__(df)

        self.product_dictionary = DictionaryDetector(
            "src/cryptoforge/discovery/resources/datasets/products.csv"
        )

    def evaluate(
        self,
        column,
        samples,
    ):

        return self.product_dictionary.score(samples)