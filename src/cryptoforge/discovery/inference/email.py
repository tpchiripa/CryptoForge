"""
=========================================================
CryptoForge Email Inferencer
=========================================================

Infers email columns.

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

from cryptoforge.discovery.resources.regex.email import (
    EMAIL_REGEX,
)


@register
class EmailInferencer(BaseSemanticInferencer):
    """
    Detect email columns.
    """

    KEYWORDS = {
        "email",
        "mail",
        "email_address",
    }

    RESULT_KEY = "email_columns"

    def __init__(self, df):
        super().__init__(df)
        self.detector = RegexDetector(EMAIL_REGEX)

    def evaluate(
        self,
        column: str,
        samples: list[str],
    ) -> float:
        """
        Evaluate how confidently the sampled values
        represent email addresses.
        """

        result = self.detector.detect(samples)

        return result.confidence