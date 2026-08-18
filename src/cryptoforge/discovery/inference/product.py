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
from cryptoforge.discovery.inference.semantic_base import (
    BaseSemanticInferencer,
)
from cryptoforge.discovery.detectors.dictionary_detector import (
    DictionaryDetector,
)
from cryptoforge.discovery.resources.paths import dataset_path
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
        self.detector = DictionaryDetector(
            dataset_path("products.csv")
        )
    def evaluate(
        self,
        column: str,
        samples: list[str],
    ) -> float:
        """
        Evaluate how confidently the sampled values
        represent product names.
        """
        result = self.detector.detect(samples)
        return result.confidence