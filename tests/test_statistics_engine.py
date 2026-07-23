"""
=========================================================
CryptoForge Statistics Engine Test
=========================================================

Tests the Statistics Engine by executing all registered
statistics calculators.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

# Importing these modules automatically registers the calculators
import cryptoforge.discovery.statistics.basic
import cryptoforge.discovery.statistics.schema
import cryptoforge.discovery.statistics.numeric
import cryptoforge.discovery.statistics.quality
import cryptoforge.discovery.statistics.timestamp

from cryptoforge.discovery.statistics.engine import StatisticsEngine


def main() -> None:
    """
    Execute the Statistics Engine against a sample dataset.
    """

    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2026-06-01",
                    "2026-06-02",
                    "2026-06-03",
                ]
            ),
            "price": [100, 101, 102],
            "quantity": [1.5, 2.1, 0.8],
            "buyer": [True, False, True],
        }
    )

    engine = StatisticsEngine(df)

    results = engine.calculate()

    print("\nRegistered Calculators")
    print("=" * 40)

    for calculator in results.keys():
        print(calculator)

    print("\nResults")
    print("=" * 40)

    for name, result in results.items():
        print(f"\n{name}")
        print(result)


if __name__ == "__main__":
    main()