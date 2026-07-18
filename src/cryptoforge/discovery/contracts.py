"""
=========================================================
CryptoForge Discovery Contracts
=========================================================

Domain models used throughout the Discovery module.

These contracts define the canonical outputs of the
Discovery Engine. They are intentionally immutable so
that downstream components (Spark, Airflow, APIs,
Power BI, etc.) can safely consume them.

Author: Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# =========================================================
# DATASET INFORMATION
# =========================================================

@dataclass(frozen=True)
class DatasetInfo:
    """
    Physical dataset metadata.
    """

    zip_file: str
    csv_file: str

    zip_size_bytes: int
    csv_size_bytes: int

    compression_ratio_percent: float


# =========================================================
# BASIC STATISTICS
# =========================================================

@dataclass(frozen=True)
class BasicStatistics:
    """
    General dataset statistics.
    """

    sample_rows: int

    column_count: int

    missing_values: int

    duplicate_rows: int

    memory_bytes: int


# =========================================================
# SCHEMA INFORMATION
# =========================================================

@dataclass(frozen=True)
class SchemaInfo:
    """
    Dataset schema definition.
    """

    columns: list[str]

    dtypes: dict[str, str]


# =========================================================
# NUMERIC STATISTICS
# =========================================================

@dataclass(frozen=True)
class NumericStatistics:
    """
    Summary statistics for numeric columns.

    Stored as a nested dictionary because the structure
    depends on the dataframe implementation.
    """

    summary: dict[str, Any] = field(default_factory=dict)


# =========================================================
# QUALITY STATISTICS
# =========================================================

@dataclass(frozen=True)
class QualityStatistics:
    """
    Data quality metrics.
    """

    missing_percentage: float

    duplicate_percentage: float

    schema_valid: bool

    quality_score: float


# =========================================================
# DISCOVERY RESULT
# =========================================================

@dataclass(frozen=True)
class DiscoveryResult:
    """
    Canonical output returned by the Discovery Engine.
    """

    dataset: DatasetInfo

    basic: BasicStatistics

    schema: SchemaInfo

    numeric: NumericStatistics

    quality: QualityStatistics