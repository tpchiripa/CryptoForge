import pandas as pd

# Register calculators
import cryptoforge.discovery.statistics.numeric

from cryptoforge.discovery.statistics.numeric import (
    NumericStatisticsCalculator,
)

print()
print("=" * 60)
print("NUMERIC STATISTICS TEST")
print("=" * 60)

df = pd.DataFrame(
    {
        "price": [100, 105, 110, 95, 120],
        "quantity": [2, 3, 5, 4, 6],
        "buyer": [True, False, True, False, True],
    }
)

calculator = NumericStatisticsCalculator(df)

result = calculator.calculate()

print()

for column, values in result.summary.items():

    print("=" * 60)
    print(column.upper())
    print("=" * 60)

    for key, value in values.items():
        print(f"{key:<15}: {value}")

    print()