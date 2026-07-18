"""
=========================================================
CryptoForge Dataset Inspector
=========================================================

Responsible for discovering and validating raw datasets.

Author: Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pandas as pd

from cryptoforge.core.settings import settings
from cryptoforge.logger import logger
from cryptoforge.discovery.contracts import DatasetInfo


class DatasetInspector:
    """
    Inspects raw datasets before profiling.
    """

    def __init__(self):

        self.raw_directory = Path(settings.paths.raw)

    def locate_dataset(self) -> Path:

        zip_files = sorted(self.raw_directory.glob("*.zip"))

        if not zip_files:
            raise FileNotFoundError(
                f"No ZIP files found in {self.raw_directory.resolve()}"
            )

        dataset = zip_files[0]

        logger.info(f"Dataset located: {dataset.name}")

        return dataset

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

        logger.info(
            f"Loaded sample with {len(dataframe):,} rows."
        )

        return dataframe
