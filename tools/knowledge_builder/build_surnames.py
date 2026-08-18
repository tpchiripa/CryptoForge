"""
=========================================================
Build Surnames Knowledge Base
=========================================================

Regenerates resources/datasets/surnames.csv from two sources,
merged (not replaced):

1. datasets/knowledge_downloads/names/census/Names_2010Census.csv
   Real US Census 2010 surname data. All ~162K surnames, title-cased
   for consistency with the rest of the file.

2. The EXISTING resources/datasets/surnames.csv, preserved.
   Keeps the hand-curated Southern African surnames (Chikore, Chirwa,
   Ndlovu, Sibanda, Van der Merwe, ...) the US Census data doesn't
   have -- merge, don't overwrite, or real coverage disappears.

The previous file is backed up to surnames.csv.bak before writing.
Revert with:
    copy /Y surnames.csv.bak surnames.csv

Run from the repo root:
    python tools\\knowledge_builder\\build_surnames.py

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SOURCE = REPO_ROOT / "datasets" / "knowledge_downloads" / "names" / "census" / "Names_2010Census.csv"
TARGET = REPO_ROOT / "src" / "cryptoforge" / "discovery" / "resources" / "datasets" / "surnames.csv"


def load_existing_surnames() -> set[str]:
    if not TARGET.exists():
        return set()
    df = pd.read_csv(TARGET)
    col = df.columns[0]
    return {str(v).strip() for v in df[col].dropna() if str(v).strip()}


def load_census_surnames() -> set[str]:
    df = pd.read_csv(SOURCE, usecols=["name"])
    return {str(v).strip().title() for v in df["name"].dropna() if str(v).strip()}


def main() -> None:
    print(f"Reading existing surnames from {TARGET} ...")
    existing = load_existing_surnames()
    print(f"  {len(existing)} existing surnames (preserved).")

    print(f"Reading Census 2010 surnames from {SOURCE} ...")
    census_surnames = load_census_surnames()
    print(f"  {len(census_surnames)} surnames found in Census data.")

    merged = sorted(existing | census_surnames)
    print(f"Merged total: {len(merged)} unique surnames.")

    if TARGET.exists():
        backup = TARGET.with_suffix(".csv.bak")
        shutil.copy2(TARGET, backup)
        print(f"Backed up existing file to {backup}")

    out_df = pd.DataFrame({"surname": merged})
    out_df.to_csv(TARGET, index=False)
    print(f"Wrote {len(merged)} surnames to {TARGET}")


if __name__ == "__main__":
    main()