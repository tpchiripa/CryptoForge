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

from dataclasses import asdict

# =========================================================
# Register Statistics Calculators
# =========================================================

import cryptoforge.discovery.statistics.basic
import cryptoforge.discovery.statistics.schema
import cryptoforge.discovery.statistics.numeric
import cryptoforge.discovery.statistics.quality
import cryptoforge.discovery.statistics.timestamp

# =========================================================
# Register Profilers
# =========================================================

import cryptoforge.discovery.profiling.column

# =========================================================
# Register Inferencers
# =========================================================

import cryptoforge.discovery.inference.primary_key
import cryptoforge.discovery.inference.identifier
import cryptoforge.discovery.inference.business_key
import cryptoforge.discovery.inference.foreign_key
import cryptoforge.discovery.inference.monotonic
import cryptoforge.discovery.inference.constant
import cryptoforge.discovery.inference.nullable
import cryptoforge.discovery.inference.categorical
import cryptoforge.discovery.inference.high_cardinality
import cryptoforge.discovery.inference.duplicate
import cryptoforge.discovery.inference.pii
import cryptoforge.discovery.inference.semantic_type

from cryptoforge.discovery.pipeline import DiscoveryPipeline


def print_section(title: str) -> None:
    """
    Prints a formatted section heading.
    """

    print(f"\n{title}")
    print("-" * 70)


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

    # =====================================================
    # Dataset
    # =====================================================

    print_section("Dataset")
    print(result.dataset)

    # =====================================================
    # Basic Statistics
    # =====================================================

    print_section("Basic Statistics")
    print(result.basic)

    # =====================================================
    # Schema
    # =====================================================

    print_section("Schema")
    print(result.schema)

    # =====================================================
    # Numeric Statistics
    # =====================================================

    print_section("Numeric Statistics")
    print(result.numeric)

    # =====================================================
    # Quality Statistics
    # =====================================================

    print_section("Quality Statistics")
    print(result.quality)

    # =====================================================
    # Timestamp Statistics
    # =====================================================

    print_section("Timestamp Statistics")
    print(result.timestamp)

    # =====================================================
    # Column Profiles
    # =====================================================

    print_section("Column Profiles")

    print(f"Total Profiles: {len(result.column_profiles)}\n")

    for index, profile in enumerate(result.column_profiles, start=1):
        print(f"[{index}]")
        print(profile)
        print()

    # =====================================================
    # Inference Results
    # =====================================================

    print_section("Inference")

    inference = asdict(result.inference)

    for field_name, value in inference.items():

        heading = field_name.replace("_", " ").title()

        print(f"\n{heading}:")
        print(value)


if __name__ == "__main__":
    main()