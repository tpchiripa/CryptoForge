"""
=========================================================
CryptoForge Knowledge Cache
=========================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


_CACHE = {}


class KnowledgeCache:

    @staticmethod
    def load(filepath):

        filepath = str(Path(filepath).resolve())

        if filepath in _CACHE:
            return _CACHE[filepath]

        df = pd.read_csv(filepath)

        column = df.columns[0]

        values = {
            str(v).strip().lower()
            for v in df[column]
            if pd.notna(v)
        }

        _CACHE[filepath] = values

        return values