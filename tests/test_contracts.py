"""
=========================================================
CryptoForge Contract Tests
=========================================================

Verifies the Discovery domain contracts.

Author: Tichaona Peter Chiripa
=========================================================
"""

from cryptoforge.discovery.contracts import (
    BasicStatistics,
    DatasetInfo,
    DiscoveryResult,
    NumericStatistics,
    QualityStatistics,
    SchemaInfo,
)


def main():

    dataset = DatasetInfo(
        zip_file="BTCUSDT-trades-2026-06.zip",
        csv_file="BTCUSDT-trades-2026-06.csv",
        zip_size_bytes=914498374,
        csv_size_bytes=9767151124,
        compression_ratio_percent=9.36,
    )

    basic = BasicStatistics(
        sample_rows=10000,
        column_count=7,
        missing_values=0,
        duplicate_rows=0,
        memory_bytes=560000,
    )

    schema = SchemaInfo(
        columns=[
            "trade_id",
            "price",
            "quantity",
            "quote_quantity",
            "timestamp",
            "is_buyer_maker",
            "is_best_match",
        ],
        dtypes={
            "trade_id": "int64",
            "price": "float64",
            "quantity": "float64",
            "quote_quantity": "float64",
            "timestamp": "datetime64[ns]",
            "is_buyer_maker": "bool",
            "is_best_match": "bool",
        },
    )

    numeric = NumericStatistics(
        summary={
            "price": {
                "min": 72000.10,
                "max": 74500.25,
                "mean": 73215.44,
            },
            "quantity": {
                "min": 0.00001,
                "max": 4.25,
                "mean": 0.0134,
            },
        }
    )

    quality = QualityStatistics(
        missing_percentage=0.0,
        duplicate_percentage=0.0,
        schema_valid=True,
        quality_score=100.0,
    )

    result = DiscoveryResult(
        dataset=dataset,
        basic=basic,
        schema=schema,
        numeric=numeric,
        quality=quality,
    )

    print("\n==============================")
    print("DiscoveryResult")
    print("==============================\n")

    print(result)

    print("\nDataset")
    print(result.dataset)

    print("\nBasic Statistics")
    print(result.basic)

    print("\nSchema")
    print(result.schema)

    print("\nQuality")
    print(result.quality)

    print("\nNumeric Summary")
    print(result.numeric.summary)


if __name__ == "__main__":
    main()