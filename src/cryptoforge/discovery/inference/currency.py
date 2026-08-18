"""
=========================================================
CryptoForge Currency Inferencer
=========================================================

Attempts to infer monetary columns AND, where possible, which
currency they're actually in.

Detection order (first match wins):
  1. A currency symbol or embedded ISO code found in the column's own
     sample values (e.g. "$100.50", "USD 100.50", "R 250.00").
  2. A sibling column in the same dataset named currency/ccy/
     currency_code/curr. If that column has exactly one distinct
     valid currency across its values, use it. If it has more than
     one, report "MIXED" rather than guessing which one is right.
  3. "UNKNOWN" -- genuinely no signal available. This is now an
     honest fallback, not the only possible outcome (previously this
     inferencer had no value-inspection logic at all and returned
     "UNKNOWN" unconditionally for every keyword match).

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import re

from cryptoforge.discovery.inference.base import BaseInferencer
from cryptoforge.discovery.inference.registry import register

_SYMBOL_MAP = {
    "$": "USD", "£": "GBP", "€": "EUR", "¥": "JPY", "₹": "INR",
    "₦": "NGN", "₽": "RUB", "₩": "KRW", "₪": "ILS", "฿": "THB",
}
_SYMBOL_PATTERN = re.compile("[" + re.escape("".join(_SYMBOL_MAP.keys())) + "]")

# "R" is too ambiguous to treat as a bare symbol (matches inside ordinary
# words) so it only counts as Rand when directly adjacent to a digit.
_RAND_PATTERN = re.compile(r"(?<![A-Za-z])R\s?\d")

# Not exhaustive ISO 4217 -- deliberately scoped to currencies plausible
# for this codebase's data (Southern/East Africa + major global). Extend
# as needed; a random uppercase 3-letter word NOT in this set is
# correctly ignored rather than misreported as a currency code.
_VALID_CODES = {
    "USD", "EUR", "GBP", "JPY", "ZAR", "AUD", "CAD", "CHF", "CNY", "INR",
    "NGN", "KES", "GHS", "BWP", "ZMW", "MWK", "MZN", "AOA", "NAD", "EGP",
    "MAD", "BRL", "MXN", "RUB", "KRW", "SGD", "HKD", "NZD", "SEK", "NOK",
    "DKK", "PLN", "TRY", "THB", "IDR", "ILS", "AED", "SAR", "QAR",
}
_CODE_PATTERN = re.compile(r"\b([A-Z]{3})\b")

_CURRENCY_COLUMN_NAMES = {"currency", "ccy", "currency_code", "curr"}


def _detect_from_values(sample_values) -> str | None:
    for v in sample_values:
        if v is None:
            continue
        s = str(v)
        sym = _SYMBOL_PATTERN.search(s)
        if sym:
            return _SYMBOL_MAP[sym.group()]
        if _RAND_PATTERN.search(s):
            return "ZAR"
        code = _CODE_PATTERN.search(s)
        if code and code.group() in _VALID_CODES:
            return code.group()
    return None


def _detect_from_sibling(df) -> str | None:
    for column in df.columns:
        if column.lower() not in _CURRENCY_COLUMN_NAMES:
            continue
        values = df[column].dropna().astype(str).str.strip().str.upper()
        uniq_valid = {v for v in values.unique() if v in _VALID_CODES}
        if len(uniq_valid) == 1:
            return next(iter(uniq_valid))
        elif len(uniq_valid) > 1:
            return "MIXED"
    return None


@register
class CurrencyInferencer(BaseInferencer):
    """
    Detect monetary columns.
    """

    KEYWORDS = {
        "price", "amount", "cost", "total", "subtotal", "balance",
        "salary", "income", "expense", "revenue", "profit", "payment",
        "tax", "vat", "fee", "charge", "quote_quantity",
    }

    def infer(self):

        self.logger.info(
            "Inferring currency columns..."
        )

        currency_columns = {}

        for column in self.df.columns:
            lower = column.lower()
            if not any(keyword in lower for keyword in self.KEYWORDS):
                continue

            detected = _detect_from_values(self.df[column].dropna().head(50).tolist())
            if detected is None:
                detected = _detect_from_sibling(self.df)
            if detected is None:
                detected = "UNKNOWN"

            currency_columns[column] = detected

        self.logger.info(
            "Detected %d monetary columns.",
            len(currency_columns),
        )

        return {
            "currency_columns": currency_columns
        }