"""
=========================================================
Build Companies Knowledge Base
=========================================================

Regenerates resources/datasets/companies.csv from two sources,
merged (not replaced):

1. SEC EDGAR company_tickers.json (fetched live -- real US SEC data,
   ~10,000 publicly-traded company names, updated periodically by the
   SEC itself). Each entry contributes both its full legal name
   ("NVIDIA CORP") and a "bare" version with the common corporate
   suffix stripped ("NVIDIA"), since real-world data columns are far
   more likely to contain the bare form.

2. The EXISTING resources/datasets/companies.csv, preserved. Keeps
   the hand-curated Southern African companies (Standard Bank, MTN,
   Shoprite, Truth Coffee, ...) that SEC EDGAR doesn't have -- SEC
   EDGAR only covers US-listed companies, so this merge, not overwrite,
   is what keeps that coverage from silently disappearing.

This makes a LIVE NETWORK REQUEST to sec.gov. The SEC requires a
descriptive User-Agent header identifying the requester (not a browser
UA string) -- replace YOUR_EMAIL below with a real contact address
before running, or the SEC's servers may reject the request.

The previous file is backed up to companies.csv.bak before writing.
Revert with:
    copy /Y companies.csv.bak companies.csv

Run from the repo root:
    python tools\\knowledge_builder\\build_companies.py

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import json
import re
import shutil
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TARGET = REPO_ROOT / "src" / "cryptoforge" / "discovery" / "resources" / "datasets" / "companies.csv"

SEC_URL = "https://www.sec.gov/files/company_tickers.json"

# REQUIRED by SEC: identify who is making the request. Replace with a
# real contact email before running -- generic/browser User-Agent
# strings can get you rate-limited or blocked.
USER_AGENT = "CryptoForge KnowledgeBuilder tpchiripa@gmail.com"

_SUFFIX_RE = re.compile(
    r",?\s+(inc\.?|incorporated|corp\.?|corporation|co\.?|company|"
    r"plc|ltd\.?|llc|l\.p\.?|lp|sa|ag|nv|se|holdings?|group)$",
    re.IGNORECASE,
)


def fetch_sec_companies() -> set[str]:
    req = urllib.request.Request(SEC_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    names: set[str] = set()
    for entry in data.values():
        title = str(entry.get("title", "")).strip()
        if not title:
            continue
        names.add(title)
        # Also add a suffix-stripped "bare" version, since real data
        # columns usually contain "Apple" not "Apple Inc.". Repeat once
        # in case of a double suffix like "X Holdings, Inc."
        bare = _SUFFIX_RE.sub("", title).strip()
        bare2 = _SUFFIX_RE.sub("", bare).strip()
        if bare2 and bare2 != title:
            names.add(bare2)
    return names


def load_existing_companies() -> set[str]:
    if not TARGET.exists():
        return set()
    import pandas as pd
    df = pd.read_csv(TARGET)
    col = df.columns[0]
    return {str(v).strip() for v in df[col].dropna() if str(v).strip()}


def main() -> None:
    import pandas as pd

    print(f"Reading existing companies from {TARGET} ...")
    existing = load_existing_companies()
    print(f"  {len(existing)} existing companies (preserved).")

    print(f"Fetching live company data from {SEC_URL} ...")
    try:
        sec_names = fetch_sec_companies()
    except Exception as exc:
        print(f"  FAILED to fetch SEC data: {exc}")
        print("  Check your internet connection, or that sec.gov isn't blocking the request.")
        print("  Existing companies.csv left untouched.")
        return
    print(f"  {len(sec_names)} company name variants found in SEC data.")

    merged = sorted(existing | sec_names)
    print(f"Merged total: {len(merged)} unique company names.")

    if TARGET.exists():
        backup = TARGET.with_suffix(".csv.bak")
        shutil.copy2(TARGET, backup)
        print(f"Backed up existing file to {backup}")

    out_df = pd.DataFrame({"company": merged})
    out_df.to_csv(TARGET, index=False)
    print(f"Wrote {len(merged)} companies to {TARGET}")


if __name__ == "__main__":
    main()