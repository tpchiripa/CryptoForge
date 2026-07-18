import pandas as pd

# importing registers the calculators
import cryptoforge.discovery.statistics.basic
import cryptoforge.discovery.statistics.schema

from cryptoforge.discovery.statistics.engine import (
    StatisticsEngine,
)


def main():

    df = pd.DataFrame(
        {
            "price": [100, 101, 102],
            "quantity": [1.5, 2.1, 0.8],
            "buyer": [True, False, True],
        }
    )

    engine = StatisticsEngine(df)

    results = engine.calculate()

    print("\nRegistered Calculators")
    print("=" * 40)

    for key in results:
        print(key)

    print("\nResults")
    print("=" * 40)

    for name, result in results.items():
        print(f"\n{name}")
        print(result)


if __name__ == "__main__":
    main()