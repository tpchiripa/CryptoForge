"""
=========================================================
CryptoForge PII Inferencer
=========================================================

Detects columns that may contain Personally
Identifiable Information (PII).

Current implementation is heuristic-based.

Future versions will use:
    • Named Entity Recognition (NER)
    • LLM-assisted inference
    • Metadata Catalog
    • Domain-specific patterns

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import re

import pandas as pd

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import InferenceRegistry


@InferenceRegistry.register
class PIIInferencer(BaseInferencer):
    """
    Detect possible PII columns.
    """

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    PHONE_PATTERN = re.compile(
        r"^\+?\d[\d\s\-\(\)]{6,}$"
    )

    def infer(self):

        self.logger.info("Inferring PII columns...")

        pii_columns = []

        for column in self.df.columns:

            series = self.df[column].dropna()

            if series.empty:
                continue

            column_name = column.lower()

            if any(
                keyword in column_name
                for keyword in (
                    "email",
                    "phone",
                    "mobile",
                    "cell",
                    "name",
                    "surname",
                    "address",
                    "passport",
                    "ssn",
                    "national",
                    "id",
                    "identity",
                )
            ):
                pii_columns.append(column)
                continue

            if pd.api.types.is_object_dtype(series):

                sample = (
                    series.astype(str)
                    .head(100)
                    .tolist()
                )

                email_matches = sum(
                    bool(self.EMAIL_PATTERN.match(v))
                    for v in sample
                )

                phone_matches = sum(
                    bool(self.PHONE_PATTERN.match(v))
                    for v in sample
                )

                if (
                    email_matches >= 5
                    or phone_matches >= 5
                ):
                    pii_columns.append(column)

        self.logger.info(
            "Detected %d PII columns.",
            len(pii_columns),
        )

        return {
            "pii_columns": pii_columns
        }