"""
=========================================================
CryptoForge Units Inferencer
=========================================================

Infers measurement units from column names.

Examples
--------
weight_kg          -> kilograms
height_cm          -> centimetres
price_usd          -> US dollars
temperature_c      -> Celsius
volume_litre       -> litres

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import re

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register


@register
class UnitsInferencer(BaseInferencer):
    """
    Detect measurement units from column names.
    """

    UNIT_PATTERNS = {

        r"\bkg\b|kilogram": "kilogram",

        r"\bg\b|gram": "gram",

        r"\bmg\b": "milligram",

        r"\bl\b|litre|liter": "litre",

        r"\bml\b": "millilitre",

        r"\bcm\b": "centimetre",

        r"\bmm\b": "millimetre",

        r"\bm\b": "metre",

        r"\bkm\b": "kilometre",

        r"\bc\b|celsius": "celsius",

        r"\bf\b|fahrenheit": "fahrenheit",

        r"\busd\b": "USD",

        r"\beur\b": "EUR",

        r"\bzar\b": "ZAR",

        r"\bgbp\b": "GBP",

        r"\bpercent\b|pct|%": "percent",

        r"\bsec\b|second": "seconds",

        r"\bmin\b|minute": "minutes",

        r"\bhour\b|hrs\b": "hours",
    }

    def infer(self):

        self.logger.info("Inferring measurement units...")

        units = {}

        for column in self.df.columns:

            name = column.lower()

            detected = None

            for pattern, unit in self.UNIT_PATTERNS.items():

                if re.search(pattern, name):

                    detected = unit

                    break

            if detected:

                units[column] = detected

        self.logger.info(
            "Detected units for %d columns.",
            len(units),
        )

        return {
            "units": units
        }