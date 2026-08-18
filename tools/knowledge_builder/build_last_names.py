"""
============================================================
CryptoForge Last Name Knowledge Base Builder
============================================================

Builds a clean surname knowledge base from a downloaded
CSV dataset.

Author:
    Tichaona Peter Chiripa
============================================================
"""

from pathlib import Path

import pandas as pd


# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

INPUT = (
    ROOT
    / "datasets"
    / "knowledge_downloads"
    / "names"
    / "last_names.csv"
)

OUTPUT = (
    ROOT
    / "src"
    / "cryptoforge"
    / "discovery"
    / "resources"
    / "knowledge"
    / "names"
    / "last_names.csv"
)


# ==========================================================
# BUILD KNOWLEDGE BASE
# ==========================================================

print("=" * 60)
print("CryptoForge Last Name Knowledge Base")
print("=" * 60)
print()

df = pd.read_csv(INPUT)

print("Columns detected:")
print(df.columns.tolist())
print()

# Automatically locate the surname column
name_column = None

for column in df.columns:
    lower = column.lower()

    if (
        "surname" in lower
        or "last" in lower
        or "family" in lower
        or "name" in lower
    ):
        name_column = column
        break

if name_column is None:
    raise ValueError(
        "Could not locate a surname column."
    )

names = (
    df[name_column]
    .astype(str)
    .str.strip()
    .str.title()
)

# Remove empty values
names = names[names != ""]
names = names[names != "Nan"]

# Remove duplicates
names = (
    names
    .drop_duplicates()
    .sort_values()
)

output = pd.DataFrame({
    "surname": names
})

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

output.to_csv(
    OUTPUT,
    index=False,
)

print(output.head(20))
print()

print(f"Last names : {len(output):,}")
print(f"Output     : {OUTPUT}")
print()
print("Knowledge base successfully built.")