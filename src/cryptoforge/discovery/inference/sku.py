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
    Detect SKU-related columns.
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

    def infer(self):

        self.logger.info(
            "Inferring SKU columns..."
        )

        sku_columns = []

        for column in self.df.columns:

            lower = column.lower()

            if any(
                keyword in lower
                for keyword in self.KEYWORDS
            ):
                sku_columns.append(column)

        self.logger.info(
            "Detected %d SKU columns.",
            len(sku_columns),
        )

        return {
            "sku_columns": sku_columns
        }