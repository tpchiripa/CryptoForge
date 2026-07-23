"""
=========================================================
CryptoForge Column Profiler Test
=========================================================

Tests profiler registration.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

import cryptoforge.discovery.profiling.column

from cryptoforge.discovery.profiling.registry import ProfilingRegistry


def main() -> None:

    print("Registered Profilers")
    print("=" * 40)

    print(ProfilingRegistry.count())

    print()

    for profiler in ProfilingRegistry.all():
        print(profiler.__name__)


if __name__ == "__main__":
    main()