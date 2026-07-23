"""
=========================================================
CryptoForge Dataset Inspector
=========================================================

Responsible for discovering, validating and loading
raw Binance datasets.

Author: Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pandas as pd

from cryptoforge.core.settings import settings
from cryptoforge.discovery.contracts import DatasetInfo
from cryptoforge.logger import logger


class DatasetInspector:
    """
    Discovers and loads Binance datasets.

    Responsibilities
    ----------------
    • Locate ZIP datasets
    • Validate archive contents
    • Extract dataset metadata
    • Load sample data
    • Apply the canonical Binance schema
    """

    BINANCE_COLUMNS = [
        "trade_id",
        "price",
        "quantity",
        "quote_quantity",
        "timestamp",
        "is_buyer_maker",
        "is_best_match",
    ]

    def __init__(self):

        self.raw_directory = Path(settings.paths.raw)

    # =====================================================
    # Dataset Discovery
    # =====================================================

    def locate_dataset(self) -> Path:

        zip_files = sorted(self.raw_directory.glob("*.zip"))

        if not zip_files:
            raise FileNotFoundError(
                f"No ZIP files found in {self.raw_directory.resolve()}"
            )

        dataset = zip_files[0]

        logger.info("Dataset located: %s", dataset.name)

        return dataset

    # =====================================================
    # Metadata Inspection
    # =====================================================

    def inspect(self) -> DatasetInfo:

        dataset = self.locate_dataset()

        with zipfile.ZipFile(dataset, "r") as archive:

            csv_files = [
                file
                for file in archive.namelist()
                if file.endswith(".csv")
            ]

            if not csv_files:
                raise RuntimeError(
                    "ZIP archive contains no CSV file."
                )

            csv_name = csv_files[0]

            info = archive.getinfo(csv_name)

            compression = round(
                info.compress_size / info.file_size * 100,
                2,
            )

        logger.info("ZIP validation successful.")

        return DatasetInfo(
            zip_file=dataset.name,
            csv_file=csv_name,
            zip_size_bytes=dataset.stat().st_size,
            csv_size_bytes=info.file_size,
            compression_ratio_percent=compression,
        )

    # =====================================================
    # Data Loading
    # =====================================================

    def load_sample(self) -> pd.DataFrame:

        dataset = self.locate_dataset()

        with zipfile.ZipFile(dataset) as archive:

            csv_name = [
                file
                for file in archive.namelist()
                if file.endswith(".csv")
            ][0]

            with archive.open(csv_name) as file:

                dataframe = pd.read_csv(
                    io.TextIOWrapper(file),
                    header=None,
                    nrows=settings.discovery.sample_rows,
                )

        dataframe = self._standardize_schema(dataframe)

        # Fixed logging statement
        logger.info(
            f"Loaded sample with {len(dataframe):,} rows."
        )

        return dataframe

    # =====================================================
    # Internal Helpers
    # =====================================================

    def _standardize_schema(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Applies the canonical Binance schema and converts
        timestamp columns to datetime.
        """

        if dataframe.shape[1] == len(self.BINANCE_COLUMNS):

            dataframe.columns = self.BINANCE_COLUMNS

        else:

            dataframe.columns = [
                f"column_{i}"
                for i in range(dataframe.shape[1])
            ]

        if "timestamp" in dataframe.columns:

            dataframe["timestamp"] = pd.to_datetime(
                dataframe["timestamp"],
                unit="us",
                errors="coerce",
            )

        return dataframe