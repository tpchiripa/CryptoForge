"""
=========================================================
CryptoForge SKU Inferencer
=========================================================

Infers Stock Keeping Unit (SKU) columns.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class SKUInferencer(BaseInferencer):
    """
    Detect SKU-related columns using column names.
    """

    KEYWORDS = {
        "sku",
        "stockkeepingunit",
        "stock_keeping_unit",
        "item_code",
        "item_number",
        "product_code",
        "product_number",
        "part_number",
        "catalog_number",
        "inventory_code",
        "inventory_number",
        "material_code",
        "material_number",
    }

    RESULT_KEY = "sku_columns"

    def infer(self) -> dict[str, list[str]]:
        """
        Infer SKU columns from column names.
        """

        self.logger.info(
            "Inferring SKU columns..."
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
            "Detected %d SKU columns.",
            len(detected),
        )

        return {
            self.RESULT_KEY: detected,
        }