"""
=========================================================
CryptoForge Configuration Manager
=========================================================

Loads the application configuration from YAML and exposes
it as strongly typed configuration objects.

Author: Tichaona Peter Chiripa
=========================================================
"""

from dataclasses import dataclass
from pathlib import Path
import yaml


# =========================================================
# Configuration Models
# =========================================================

@dataclass
class ProjectConfig:
    name: str
    version: str
    author: str


@dataclass
class PathsConfig:
    raw: str
    archive: str
    quarantine: str
    bronze: str
    silver: str
    gold: str


@dataclass
class MetadataConfig:
    directory: str


@dataclass
class ReportsConfig:
    directory: str


@dataclass
class LogsConfig:
    directory: str


@dataclass
class SparkConfig:
    app_name: str
    master: str
    partitions: int


@dataclass
class DiscoveryConfig:
    sample_rows: int


# =========================================================
# Settings Loader
# =========================================================

class Settings:

    def __init__(self, config_path: str = "configs/config.yaml"):

        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}"
            )

        with open(config_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        self.project = ProjectConfig(**config["project"])
        self.paths = PathsConfig(**config["paths"])
        self.metadata = MetadataConfig(**config["metadata"])
        self.reports = ReportsConfig(**config["reports"])
        self.logs = LogsConfig(**config["logs"])
        self.spark = SparkConfig(**config["spark"])
        self.discovery = DiscoveryConfig(**config["discovery"])


# =========================================================
# Global Settings Instance
# =========================================================

settings = Settings()