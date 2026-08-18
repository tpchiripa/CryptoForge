"""
=========================================================
Build Products Knowledge Base
=========================================================

Regenerates resources/datasets/products.csv from two sources,
merged (not replaced):

1. Google's official Product Taxonomy (fetched live from google.com --
   ~6,600 real product category names used across Google Shopping/
   Merchant Center, e.g. "Laptop Sleeves", "Hoodies & Sweatshirts",
   "Dog Food"). This is the leaf name from each hierarchical category
   path, not the full path -- "Bird Food" not "Animals & Pet Supplies >
   Pet Supplies > Bird Supplies > Bird Food".

2. The EXISTING resources/datasets/products.csv, preserved. Keeps
   whatever generic terms (Laptop, Coffee, Shoes, ...) were already
   curated there.

HONEST LIMITATION: DictionaryDetector does exact (lowercased) string
matching. Many Google taxonomy leaves are multi-word phrases like
"Hoodies & Sweatshirts" or "Non-prescription Cat Food" -- these will
only match a data value that is that *exact* phrase, not a data value
that just says "Hoodie". This still meaningfully expands single-word
and short-phrase coverage (a large share of leaf categories ARE single
words: "Coffee", "Shoes", "Backpacks", ...), but it isn't a fuzzy or
substring matcher. If false negatives on multi-word categories turn out
to matter in practice, the real fix is a smarter detector (token overlap
or substring matching), not a bigger dictionary -- flagging this now
rather than overselling what this script buys you.

This makes a LIVE NETWORK REQUEST to google.com.

The previous file is backed up to products.csv.bak before writing.
Revert with:
    copy /Y products.csv.bak products.csv

Run from the repo root:
    python tools\\knowledge_builder\\build_products.py

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TARGET = REPO_ROOT / "src" / "cryptoforge" / "discovery" / "resources" / "datasets" / "products.csv"

TAXONOMY_URL = "https://www.google.com/basepages/producttype/taxonomy-with-ids.en-US.txt"
USER_AGENT = "CryptoForge KnowledgeBuilder (data reference build)"


def fetch_taxonomy_leaves() -> set[str]:
    req = urllib.request.Request(TAXONOMY_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8")

    leaves: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or " - " not in line:
            continue
        _id, path = line.split(" - ", 1)
        leaf = path.split(">")[-1].strip()
        if leaf:
            leaves.add(leaf)
    return leaves


def load_existing_products() -> set[str]:
    if not TARGET.exists():
        return set()
    import pandas as pd
    df = pd.read_csv(TARGET)
    col = df.columns[0]
    return {str(v).strip() for v in df[col].dropna() if str(v).strip()}


def main() -> None:
    import pandas as pd

    print(f"Reading existing products from {TARGET} ...")
    existing = load_existing_products()
    print(f"  {len(existing)} existing products (preserved).")

    print(f"Fetching live Google Product Taxonomy from {TAXONOMY_URL} ...")
    try:
        taxonomy_leaves = fetch_taxonomy_leaves()
    except Exception as exc:
        print(f"  FAILED to fetch taxonomy data: {exc}")
        print("  Check your internet connection, or that google.com isn't blocking the request.")
        print("  Existing products.csv left untouched.")
        return
    print(f"  {len(taxonomy_leaves)} category leaf names found.")

    merged = sorted(existing | taxonomy_leaves)
    print(f"Merged total: {len(merged)} unique product terms.")

    if TARGET.exists():
        backup = TARGET.with_suffix(".csv.bak")
        shutil.copy2(TARGET, backup)
        print(f"Backed up existing file to {backup}")

    out_df = pd.DataFrame({"product": merged})
    out_df.to_csv(TARGET, index=False)
    print(f"Wrote {len(merged)} products to {TARGET}")


if __name__ == "__main__":
    main()