"""
=========================================================
CryptoForge Confidence Scorer
=========================================================

Produces a confidence score for inferred metadata.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations


class ConfidenceScorer:
    """
    Combines multiple evidence sources into a single score.
    """

    def __init__(
        self,
        keyword_weight: float = 0.40,
        regex_weight: float = 0.60,
    ):

        self.keyword_weight = keyword_weight
        self.regex_weight = regex_weight

    def score(
        self,
        keyword_match: bool,
        regex_score: float,
    ) -> float:
        """
        Compute a confidence score between 0 and 1.
        """

        keyword_component = (
            self.keyword_weight
            if keyword_match
            else 0.0
        )

        regex_component = (
            regex_score * self.regex_weight
        )

        confidence = (
            keyword_component
            + regex_component
        )

        return round(min(confidence, 1.0), 3)

    def accepted(
        self,
        confidence: float,
        threshold: float = 0.75,
    ) -> bool:
        """
        Determine whether a confidence score passes the threshold.
        """

        return confidence >= threshold