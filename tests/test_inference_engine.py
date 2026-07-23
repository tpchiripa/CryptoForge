"""
CryptoForge Inference Engine Test
"""

import pandas as pd

from cryptoforge.discovery.inference.engine import (
    InferenceEngine,
)


def main():

    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "price": [100, 101, 102],
        }
    )

    results = InferenceEngine(df).infer()

    print()
    print("=" * 60)
    print("INFERENCE RESULTS")
    print("=" * 60)

    print(results)


if __name__ == "__main__":
    main()