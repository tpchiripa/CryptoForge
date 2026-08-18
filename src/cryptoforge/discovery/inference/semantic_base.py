"""
=========================================================
CryptoForge Base Semantic Inferencer
=========================================================

Reusable base class for semantic inferencers.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.base import BaseInferencer

from cryptoforge.discovery.detectors.keyword_detector import KeywordDetector
from cryptoforge.discovery.detectors.sample_detector import SampleDetector
from cryptoforge.discovery.detectors.confidence_scorer import ConfidenceScorer


class BaseSemanticInferencer(BaseInferencer):
    """
    Shared implementation used by semantic inferencers.
    """

    KEYWORDS = set()

    RESULT_KEY = ""

    def evaluate(
        self,
        column: str,
        samples: list[str],
    ) -> float:
        """
        Override inside subclasses.
        """
        raise NotImplementedError

    def infer(self):

        self.logger.info(
            "Inferring semantic columns..."
        )

        keyword_detector = KeywordDetector(
            self.KEYWORDS
        )

        sampler = SampleDetector(self.df)

        scorer = ConfidenceScorer()

        detected = []

        for column in self.df.columns:

            keyword_match = keyword_detector.matches(column)

            samples = sampler.sample(column)

            semantic_score = self.evaluate(
                column,
                samples,
            )

            confidence = scorer.score(
                keyword_match,
                semantic_score,
            )

            self.logger.debug(
                "%s -> keyword=%s semantic=%.2f confidence=%.2f",
                column,
                keyword_match,
                semantic_score,
                confidence,
            )

            if scorer.accepted(confidence):
                detected.append(column)

        self.logger.info(
            "Detected %d semantic columns.",
            len(detected),
        )

        return {
            self.RESULT_KEY: detected
        }