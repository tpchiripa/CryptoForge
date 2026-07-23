"""
=========================================================
CryptoForge Profiling Engine Test
=========================================================

Author:
    Tichaona Peter Chiripa
=========================================================
"""

import pandas as pd

# Import registers profiler automatically
import cryptoforge.discovery.profiling.column

from cryptoforge.discovery.profiling.engine import ProfilingEngine


def main():

    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                "2026-06-01",
                periods=3,
            ),
            "price": [100, 101, 102],
            "quantity": [1.5, 2.1, 0.8],
            "buyer": [True, False, True],
        }
    )

    engine = ProfilingEngine(df)

    profiles = engine.profile()

    print()

    print("=" * 60)
    print("COLUMN PROFILES")
    print("=" * 60)

    for profile in profiles:

        print(profile)

    print()

    print(f"Total profiles: {len(profiles)}")


if __name__ == "__main__":
    main()