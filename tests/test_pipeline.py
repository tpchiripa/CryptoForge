"""
=========================================================
CryptoForge Discovery Pipeline Test
=========================================================

Executes the complete Discovery Pipeline and displays
all outputs produced by the pipeline.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

# Register Statistics Calculators
import cryptoforge.discovery.statistics.basic
import cryptoforge.discovery.statistics.schema
import cryptoforge.discovery.statistics.numeric
import cryptoforge.discovery.statistics.quality
import cryptoforge.discovery.statistics.timestamp

# Register Profilers
import cryptoforge.discovery.profiling.column

# Register Inferencers
import cryptoforge.discovery.inference.primary_key

from cryptoforge.discovery.pipeline import DiscoveryPipeline


def main() -> None:
    """
    Execute the Discovery Pipeline and display the results.
    """

    pipeline = DiscoveryPipeline()

    result = pipeline.run()

    print()
    print("=" * 70)
    print("DISCOVERY RESULT")
    print("=" * 70)

    # -------------------------------------------------
    # Dataset
    # -------------------------------------------------

    print("\nDataset")
    print("-" * 70)
    print(result.dataset)

    # -------------------------------------------------
    # Basic Statistics
    # -------------------------------------------------

    print("\nBasic Statistics")
    print("-" * 70)
    print(result.basic)

    # -------------------------------------------------
    # Schema
    # -------------------------------------------------

    print("\nSchema")
    print("-" * 70)
    print(result.schema)

    # -------------------------------------------------
    # Numeric Statistics
    # -------------------------------------------------

    print("\nNumeric Statistics")
    print("-" * 70)
    print(result.numeric)

    # -------------------------------------------------
    # Quality Statistics
    # -------------------------------------------------

    print("\nQuality Statistics")
    print("-" * 70)
    print(result.quality)

    # -------------------------------------------------
    # Timestamp Statistics
    # -------------------------------------------------

    print("\nTimestamp Statistics")
    print("-" * 70)
    print(result.timestamp)

    # -------------------------------------------------
    # Column Profiles
    # -------------------------------------------------

    print("\nColumn Profiles")
    print("-" * 70)

    print(f"Total Profiles: {len(result.column_profiles)}")
    print()

    for index, profile in enumerate(result.column_profiles, start=1):
        print(f"[{index}] {profile}")
        print()

    # -------------------------------------------------
    # Inference Results
    # -------------------------------------------------

    print("\nInference")
    print("-" * 70)

    print("Primary Keys:")
    print(result.inference.primary_keys)

    print()

    print("Identifiers:")
    print(result.inference.identifiers)

    print()

    print("Categorical Columns:")
    print(result.inference.categorical_columns)

    print()

    print("Monotonic Columns:")
    print(result.inference.monotonic_columns)

    print()

    print("Constant Columns:")
    print(result.inference.constant_columns)

    print()

    print("Nullable Columns:")
    print(result.inference.nullable_columns)

    print()

    print("High Cardinality Columns:")
    print(result.inference.high_cardinality_columns)


if __name__ == "__main__":
    main()