"""
Enterprise Logging Configuration
"""

import logging
import logging.config
from pathlib import Path

import yaml


def configure_logging():
    """
    Configure logging from YAML configuration.
    """

    config_file = Path("configs/logging.yaml")

    if not config_file.exists():
        raise FileNotFoundError(
            f"Logging configuration not found: {config_file}"
        )

    Path("logs").mkdir(exist_ok=True)

    with open(config_file, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.
    """
    return logging.getLogger(name)