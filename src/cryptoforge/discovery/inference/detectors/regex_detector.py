"""
=========================================================
CryptoForge Regex Detector
=========================================================

Reusable regex-based detector for semantic inferencers.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import re

import pandas as pd


class RegexDetector:
    """
    Detects semantic columns by analysing values rather than
    relying on column names.

    Parameters
    ----------
    pattern:
        Compiled regular expression.

    threshold:
        Minimum percentage of sampled rows that must match.

    sample_size:
        Maximum number of rows inspected.
    """

    def __init__(
        self,
        pattern: str,
        threshold: float = 0.80,
        sample_size: int = 500,
    ) -> None:

        self.pattern = re.compile(pattern)

        self.threshold = threshold

        self.sample_size = sample_size

    def detect(self, dataframe: pd.DataFrame) -> list[str]:

        detected = []

        for column in dataframe.columns:

            series = (
                dataframe[column]
                .dropna()
                .astype(str)
                .head(self.sample_size)
            )

            if series.empty:
                continue

            matches = sum(
                bool(self.pattern.fullmatch(value.strip()))
                for value in series
            )

            confidence = matches / len(series)

            if confidence >= self.threshold:
                detected.append(column)

        return detected