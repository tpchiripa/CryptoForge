import pandas as pd

from cryptoforge.discovery.statistics.basic import (
    BasicStatisticsCalculator,
)


def main():

    df = pd.DataFrame(
        {
            "price": [10, 20, 30],
            "qty": [1, 2, 3],
        }
    )

    calculator = BasicStatisticsCalculator(df)

    result = calculator.calculate()

    print(result)


if __name__ == "__main__":
    main()