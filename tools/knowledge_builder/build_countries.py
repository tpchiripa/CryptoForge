from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

INPUT = (
    ROOT
    / "datasets"
    / "knowledge_downloads"
    / "countryInfo.txt"
)

OUTPUT = (
    ROOT
    / "src"
    / "cryptoforge"
    / "discovery"
    / "resources"
    / "knowledge"
    / "countries"
    / "countries.csv"
)

records = []

with open(INPUT, encoding="utf-8") as f:

    for line in f:

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        parts = line.split("\t")

        # GeoNames country rows should have at least 5 columns
        if len(parts) < 5:
            continue

        try:

            iso2 = parts[0].strip()
            iso3 = parts[1].strip()
            country = parts[4].strip()

            if country:

                records.append(
                    {
                        "country": country,
                        "iso2": iso2,
                        "iso3": iso3,
                    }
                )

        except Exception:
            continue


df = (
    pd.DataFrame(records)
    .drop_duplicates(subset=["country"])
    .sort_values("country")
    .reset_index(drop=True)
)

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

df.to_csv(
    OUTPUT,
    index=False,
)

print("=" * 60)
print("CryptoForge Country Knowledge Base")
print("=" * 60)
print()

print(df.head(10))
print()

print("Countries :", len(df))
print("Output    :", OUTPUT)