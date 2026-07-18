import pandas as pd

from cryptoforge.discovery.statistics.schema import (
    SchemaStatisticsCalculator,
)


def main():

    df = pd.DataFrame(
        {
            "price": [10.5, 20.4],
            "quantity": [1.2, 3.4],
            "buyer": [True, False],
        }
    )

    calculator = SchemaStatisticsCalculator(df)

    schema = calculator.calculate()

    print("\nColumns")
    print(schema.columns)

    print("\nDtypes")
    print(schema.dtypes)


if __name__ == "__main__":
    main()