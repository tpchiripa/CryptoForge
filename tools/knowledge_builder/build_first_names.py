"""
=========================================================
Build First Names Knowledge Base
=========================================================

Regenerates resources/datasets/first_names.csv from two sources,
merged (not replaced):

1. datasets/knowledge_downloads/names/baby_names.csv
   Real SSA baby-name data (columns: year, name, percent, sex).
   Unique names across all years, deduped case-insensitively.

2. The EXISTING resources/datasets/first_names.csv, preserved.
   This keeps the hand-curated Southern African names (Chipo, Farai,
   Nomsa, Tendai, ...) that the SSA dataset doesn't have -- a straight
   overwrite would silently delete real, deliberately-added coverage.

The previous file is backed up to first_names.csv.bak before writing,
so this is a one-command revert if the output ever looks wrong:
    copy /Y first_names.csv.bak first_names.csv

Run from the repo root:
    python tools\\knowledge_builder\\build_first_names.py

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE = REPO_ROOT / "datasets" / "knowledge_downloads" / "names" / "baby_names.csv"
TARGET = REPO_ROOT / "src" / "cryptoforge" / "discovery" / "resources" / "datasets" / "first_names.csv"


def load_existing_names() -> set[str]:
    if not TARGET.exists():
        return set()
    df = pd.read_csv(TARGET)
    col = df.columns[0]
    return {str(v).strip() for v in df[col].dropna() if str(v).strip()}


def load_ssa_names() -> set[str]:
    df = pd.read_csv(SOURCE, usecols=["name"])
    return {str(v).strip().title() for v in df["name"].dropna() if str(v).strip()}


def main() -> None:
    print(f"Reading existing names from {TARGET} ...")
    existing = load_existing_names()
    print(f"  {len(existing)} existing names (preserved).")

    print(f"Reading SSA baby names from {SOURCE} ...")
    ssa_names = load_ssa_names()
    print(f"  {len(ssa_names)} unique names found in SSA data.")

    merged = sorted(existing | ssa_names)
    print(f"Merged total: {len(merged)} unique first names.")

    if TARGET.exists():
        backup = TARGET.with_suffix(".csv.bak")
        shutil.copy2(TARGET, backup)
        print(f"Backed up existing file to {backup}")

    out_df = pd.DataFrame({"name": merged})
    out_df.to_csv(TARGET, index=False)
    print(f"Wrote {len(merged)} names to {TARGET}")


if __name__ == "__main__":
    main()