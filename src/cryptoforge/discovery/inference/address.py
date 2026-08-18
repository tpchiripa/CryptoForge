"""
=========================================================
CryptoForge Address Inferencer
=========================================================

Infers address columns.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.registry import register
from cryptoforge.discovery.inference.semantic_base import (
    BaseSemanticInferencer,
)

from cryptoforge.discovery.detectors.regex_detector import (
    RegexDetector,
)

from cryptoforge.discovery.resources.regex.address import (
    ADDRESS_REGEX,
)


@register
class AddressInferencer(BaseSemanticInferencer):
    """
    Detect address columns.
    """

    KEYWORDS = {
        "address",
        "street",
        "location",
        "postal",
        "postcode",
        "zip",
        "zipcode",
        "city",
        "province",
        "state",
        "physical_address",
        "billing_address",
        "shipping_address",
    }

    RESULT_KEY = "address_columns"

    def __init__(self, df):
        super().__init__(df)
        self.detector = RegexDetector(ADDRESS_REGEX)

    def evaluate(
        self,
        column: str,
        samples: list[str],
    ) -> float:
        """
        Evaluate how confidently the sampled values
        represent addresses.
        """

        result = self.detector.detect(samples)

        return result.confidence