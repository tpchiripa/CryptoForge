"""
=========================================================
CryptoForge Phone Inferencer
=========================================================

Infers phone number columns.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.registry import register
from cryptoforge.discovery.inference.semantic_base import BaseSemanticInferencer

from cryptoforge.discovery.detectors.regex_detector import RegexDetector

from cryptoforge.discovery.resources.regex.phone import PHONE_REGEX


@register
class PhoneInferencer(BaseSemanticInferencer):
    """
    Detect phone number columns.
    """

    KEYWORDS = {
        "phone",
        "telephone",
        "mobile",
        "cell",
        "cellphone",
        "contact",
        "contact_number",
        "contact_no",
        "tel",
    }

    RESULT_KEY = "phone_columns"

    def __init__(self, df):
        super().__init__(df)
        self.detector = RegexDetector(PHONE_REGEX)

    def evaluate(
        self,
        column: str,
        samples: list[str],
    ) -> float:

        return self.detector.score(samples)