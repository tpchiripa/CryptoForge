import pandas as pd

import cryptoforge.discovery.statistics.timestamp

from cryptoforge.discovery.statistics.timestamp import (
    TimestampStatisticsCalculator,
)


print()
print("=" * 60)
print("TIMESTAMP STATISTICS TEST")
print("=" * 60)

df = pd.DataFrame(
    {
        "timestamp": pd.to_datetime(
            [
                "2026-06-01",
                "2026-06-02",
                "2026-06-03",
                "2026-06-04",
                "2026-06-05",
            ]
        ),
        "price": [100, 101, 102, 103, 104],
    }
)

calculator = TimestampStatisticsCalculator(df)

result = calculator.calculate()

for column, stats in result.summary.items():

    print()

    print("=" * 60)

    print(column.upper())

    print("=" * 60)

    for key, value in stats.items():

        print(f"{key:<18}: {value}")