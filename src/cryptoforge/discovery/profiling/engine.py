"""
=========================================================
CryptoForge Profiling Engine
=========================================================

Executes all registered profilers.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import pandas as pd

from cryptoforge.logger import get_logger

from cryptoforge.discovery.profiling.registry import ProfilingRegistry


class ProfilingEngine:
    """
    Executes every registered profiler.
    """

    def __init__(self, dataframe: pd.DataFrame):

        self.logger = get_logger(__name__)

        self.dataframe = dataframe

    def profile(self) -> list:

        self.logger.info(
            "Executing Profiling Engine..."
        )

        profiles = []

        for profiler in ProfilingRegistry.all():

            self.logger.info(
                "Running %s...",
                profiler.__name__,
            )

            instance = profiler(self.dataframe)

            result = instance.profile()

            if isinstance(result, list):

                profiles.extend(result)

            elif result is not None:

                profiles.append(result)

        self.logger.info(
            "Profiling Engine completed successfully."
        )

        return profiles