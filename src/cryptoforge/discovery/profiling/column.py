"""
=========================================================
CryptoForge Column Profiler
=========================================================

Profiles every dataframe column and produces
ColumnProfile contracts.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_string_dtype,
)

from cryptoforge.discovery.contracts import ColumnProfile
from cryptoforge.discovery.profiling.base import BaseProfiler
from cryptoforge.discovery.profiling.registry import ProfilingRegistry
from cryptoforge.logger import get_logger


@ProfilingRegistry.register
class ColumnProfiler(BaseProfiler):
    """
    Profiles every dataframe column.
    """

    def __init__(self, dataframe):

        super().__init__(dataframe)

        self.logger = get_logger(self.__class__.__name__)

    def profile(self) -> list[ColumnProfile]:

        self.logger.info("Profiling dataframe columns...")

        profiles: list[ColumnProfile] = []

        total_rows = len(self.df)

        for column in self.df.columns:

            series = self.df[column]

            missing = int(series.isna().sum())

            unique = int(series.nunique(dropna=True))

            profile = ColumnProfile(
                name=str(column),
                dtype=str(series.dtype),
                nullable=missing > 0,
                missing_values=missing,
                missing_percentage=(
                    missing / total_rows * 100
                    if total_rows
                    else 0.0
                ),
                unique_values=unique,
                cardinality=(
                    unique / total_rows
                    if total_rows
                    else 0.0
                ),
                memory_bytes=int(series.memory_usage(deep=True)),
                sample_values=series.dropna().head(5).tolist(),
                is_numeric=is_numeric_dtype(series),
                is_boolean=is_bool_dtype(series),
                is_datetime=is_datetime64_any_dtype(series),
                is_text=is_string_dtype(series),
            )

            profiles.append(profile)

        self.logger.info(
            "Generated profiles for %d columns.",
            len(profiles),
        )

        return profiles