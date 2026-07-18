from cryptoforge.discovery.contracts import (
    DatasetInfo,
    SampleStatistics,
    SchemaInfo,
    NumericStatistics,
    DiscoveryResult,
)

dataset = DatasetInfo(
    zip_file="BTCUSDT.zip",
    csv_file="BTCUSDT.csv",
    zip_size_bytes=100,
    csv_size_bytes=500,
    compression_ratio_percent=20.0,
)

stats = SampleStatistics(
    sample_rows=10000,
    column_count=7,
    missing_values=0,
    duplicate_rows=0,
    memory_bytes=102400,
)

schema = SchemaInfo(
    columns=["price", "quantity"],
    dtypes={"price": "float64", "quantity": "float64"},
)

numeric = NumericStatistics()

result = DiscoveryResult(
    dataset=dataset,
    statistics=stats,
    schema=schema,
    numeric=numeric,
)

print(result)
