"""
CryptoForge Primary Key Inferencer Test
"""

import pandas as pd

import cryptoforge.discovery.inference.primary_key

from cryptoforge.discovery.inference.engine import (
    InferenceEngine,
)


def main():

    df = pd.DataFrame(
        {
            "trade_id": [1001, 1002, 1003, 1004],
            "price": [73000, 73000, 73001, 73001],
            "quantity": [1, 2, 3, 4],
        }
    )

    results = InferenceEngine(df).infer()

    print()
    print("=" * 60)
    print("PRIMARY KEY INFERENCE")
    print("=" * 60)

    for name, result in results.items():

        print()
        print(name)
        print(result)


if __name__ == "__main__":
    main()