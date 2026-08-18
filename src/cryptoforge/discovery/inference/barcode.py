"""
=========================================================
CryptoForge Barcode Inferencer
=========================================================

Infers barcode columns.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class BarcodeInferencer(BaseInferencer):
    """
    Detect barcode-related columns using column names.
    """

    KEYWORDS = {
        "barcode",
        "bar_code",
        "ean",
        "ean8",
        "ean13",
        "upc",
        "upc_a",
        "upc_e",
        "gtin",
        "gtin8",
        "gtin12",
        "gtin13",
        "gtin14",
        "isbn",
        "issn",
        "code128",
        "qr_code",
    }

    RESULT_KEY = "barcode_columns"

    def infer(self) -> dict[str, list[str]]:
        """
        Infer barcode columns from column names.
        """

        self.logger.info(
            "Inferring barcode columns..."
        )

        detected: list[str] = []

        for column in self.df.columns:

            lower = column.lower()

            if any(
                keyword in lower
                for keyword in self.KEYWORDS
            ):
                detected.append(column)

        self.logger.info(
            "Detected %d barcode columns.",
            len(detected),
        )

        return {
            self.RESULT_KEY: detected,
        }