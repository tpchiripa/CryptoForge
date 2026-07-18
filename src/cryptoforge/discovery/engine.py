
"""
CryptoForge Discovery Engine v1.0
Profiles a raw Binance ZIP dataset and generates Markdown + JSON metadata.
"""
import io,json,zipfile
from pathlib import Path
import pandas as pd

RAW_DATA_DIR=Path("data/raw")
REPORT_DIR=Path("docs")
METADATA_DIR=Path("metadata")
REPORT_FILE=REPORT_DIR/"Dataset_Report.md"
METADATA_FILE=METADATA_DIR/"dataset_profile.json"
SAMPLE_ROWS=10000

BINANCE_COLUMNS=[
    "trade_id","price","quantity","quote_quantity",
    "timestamp","is_buyer_maker","is_best_match"
]

def fmt_bytes(n:int)->str:
    units=["B","KB","MB","GB","TB"]
    i=0
    n=float(n)
    while n>=1024 and i<len(units)-1:
        n/=1024;i+=1
    return f"{n:.2f} {units[i]}"

def main():
    REPORT_DIR.mkdir(exist_ok=True)
    METADATA_DIR.mkdir(exist_ok=True)

    zips=list(RAW_DATA_DIR.glob("*.zip"))
    if not zips:
        raise FileNotFoundError(f"No zip files in {RAW_DATA_DIR.resolve()}")

    zp=zips[0]
    print(f"Analyzing {zp.name}")

    with zipfile.ZipFile(zp) as z:
        csvs=[n for n in z.namelist() if n.endswith(".csv")]
        if not csvs:
            raise RuntimeError("No CSV found inside ZIP")
        csv_name=csvs[0]
        info=z.getinfo(csv_name)
        with z.open(csv_name) as f:
            df=pd.read_csv(io.TextIOWrapper(f),header=None,nrows=SAMPLE_ROWS)

    if df.shape[1]==len(BINANCE_COLUMNS):
        df.columns=BINANCE_COLUMNS
    else:
        df.columns=[f"column_{i}" for i in range(df.shape[1])]

    if "timestamp" in df.columns:
        try:
            df["timestamp"]=pd.to_datetime(df["timestamp"],unit="ms",errors="coerce")
        except Exception:
            pass

    numeric=df.select_dtypes(include="number")
    metadata={
        "zip_file":zp.name,
        "csv_file":csv_name,
        "zip_size_bytes":zp.stat().st_size,
        "csv_size_bytes":info.file_size,
        "compression_ratio_percent":round(info.compress_size/info.file_size*100,2),
        "sample_rows":len(df),
        "columns":list(df.columns),
        "column_count":df.shape[1],
        "missing_values":int(df.isna().sum().sum()),
        "duplicate_rows":int(df.duplicated().sum()),
        "memory_bytes":int(df.memory_usage(deep=True).sum()),
        "dtypes":{c:str(t) for c,t in df.dtypes.items()},
        "numeric_summary":numeric.describe().to_dict() if not numeric.empty else {}
    }
    METADATA_FILE.write_text(json.dumps(metadata,indent=4,default=str),encoding="utf-8")

    report=f"""# CryptoForge Dataset Discovery Report

## Dataset
|Property|Value|
|---|---|
|ZIP|{zp.name}|
|CSV|{csv_name}|
|ZIP Size|{fmt_bytes(zp.stat().st_size)}|
|CSV Size|{fmt_bytes(info.file_size)}|
|Compression|{metadata['compression_ratio_percent']}%|

## Sample
|Metric|Value|
|---|---|
|Rows|{len(df):,}|
|Columns|{df.shape[1]}|
|Missing|{metadata['missing_values']}|
|Duplicates|{metadata['duplicate_rows']}|
|Memory|{fmt_bytes(metadata['memory_bytes'])}|

## Columns

{", ".join(df.columns)}

## Data Types

```
{df.dtypes.to_string()}
```

## First 10 Rows

```
{df.head(10).to_string(index=False)}
```

## Numeric Summary

```
{numeric.describe().to_string() if not numeric.empty else "No numeric columns detected."}
```

## Recommendations

- Bronze: preserve raw data as immutable parquet/delta.
- Silver: validate schema, timestamps, duplicates and nulls.
- Gold: build hourly, daily, VWAP, volatility and liquidity aggregates.
"""
    REPORT_FILE.write_text(report,encoding="utf-8")
    print("Done.")
    print(REPORT_FILE.resolve())
    print(METADATA_FILE.resolve())

if __name__=="__main__":
    main()
