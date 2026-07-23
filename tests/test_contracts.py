"""
=========================================================
CryptoForge Contracts Test
=========================================================

Verifies that all Discovery contracts can be instantiated.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from cryptoforge.discovery.contracts import (
    DatasetInfo,
    BasicStatistics,
    SchemaInfo,
    NumericStatistics,
    QualityStatistics,
    TimestampStatistics,
    ColumnProfile,
    DiscoveryResult,
)


def main():

    dataset = DatasetInfo(
        zip_file="btc.zip",
        csv_file="btc.csv",
        zip_size_bytes=100,
        csv_size_bytes=500,
        compression_ratio_percent=20.0,
    )

    basic = BasicStatistics(
        sample_rows=10000,
        column_count=7,
        missing_values=0,
        duplicate_rows=0,
        memory_bytes=420132,
    )

    schema = SchemaInfo(
        columns=["price", "quantity"],
        dtypes={
            "price": "float64",
            "quantity": "float64",
        },
    )

    numeric = NumericStatistics(
        summary={}
    )

    quality = QualityStatistics(
        missing_values=0,
        missing_percentage=0.0,
        duplicate_rows=0,
        duplicate_percentage=0.0,
        unique_rows=10000,
        completeness_score=100.0,
        quality_score=100.0,
    )

    timestamp = TimestampStatistics(
        summary={}
    )

    profile = ColumnProfile(
        name="price",
        dtype="float64",
        nullable=False,
        missing_values=0,
        missing_percentage=0.0,
        unique_values=1122,
        cardinality=0.1122,
        memory_bytes=80000,
        sample_values=[
            73674.39,
            73680.11,
            73710.50,
        ],
        is_numeric=True,
    )

    result = DiscoveryResult(
        dataset=dataset,
        basic=basic,
        schema=schema,
        numeric=numeric,
        quality=quality,
        timestamp=timestamp,
        column_profiles=[profile],
    )

    print("\nContracts Test")
    print("=" * 60)

    print(result)

    print("\nColumn Profiles")
    print("=" * 60)

    for column in result.column_profiles:
        print(column)


if __name__ == "__main__":
    main()