"""
=========================================================
CryptoForge Discovery Contracts
=========================================================

Domain models used throughout the Discovery module.

These contracts define the canonical outputs of the
Discovery Engine. They are intentionally immutable so
that downstream components (Spark, Airflow, APIs,
Power BI, etc.) can safely consume them.

Author:
    Tichaona Peter Chiripa
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
    """

    summary: dict[str, Any] = field(default_factory=dict)


# =========================================================
# QUALITY STATISTICS
# =========================================================

@dataclass(frozen=True)
class QualityStatistics:
    """
    Dataset quality metrics.
    """

    missing_values: int
    missing_percentage: float

    duplicate_rows: int
    duplicate_percentage: float

    unique_rows: int

    completeness_score: float
    quality_score: float


# =========================================================
# TIMESTAMP STATISTICS
# =========================================================

@dataclass(frozen=True)
class TimestampStatistics:
    """
    Statistics for timestamp columns.
    """

    summary: dict[str, Any] = field(default_factory=dict)


# =========================================================
# COLUMN PROFILE
# =========================================================

@dataclass(frozen=True)
class ColumnProfile:
    """
    Profile describing a single dataset column.
    """

    name: str
    dtype: str

    nullable: bool

    missing_values: int
    missing_percentage: float

    unique_values: int
    cardinality: float

    memory_bytes: int

    sample_values: list[Any] = field(default_factory=list)

    is_numeric: bool = False
    is_boolean: bool = False
    is_datetime: bool = False
    is_text: bool = False


# =========================================================
# INFERENCE RESULT
# =========================================================

@dataclass(frozen=True)
class InferenceResult:
    """
    Metadata inferred from the dataset.

    Each inferencer contributes one or more outputs to
    this canonical Discovery contract.
    """

    # -----------------------------------------------------
    # Keys
    # -----------------------------------------------------

    primary_keys: list[str] = field(default_factory=list)

    identifiers: list[str] = field(default_factory=list)

    business_keys: list[str] = field(default_factory=list)

    foreign_keys: list[dict[str, Any]] = field(default_factory=list)

    # -----------------------------------------------------
    # Structural Characteristics
    # -----------------------------------------------------

    categorical_columns: list[str] = field(default_factory=list)

    monotonic_columns: list[str] = field(default_factory=list)

    constant_columns: list[str] = field(default_factory=list)

    nullable_columns: list[str] = field(default_factory=list)

    high_cardinality_columns: list[str] = field(default_factory=list)

    duplicate_columns: list[str] = field(default_factory=list)

    # -----------------------------------------------------
    # Governance
    # -----------------------------------------------------

    pii_columns: list[str] = field(default_factory=list)

    # -----------------------------------------------------
    # Contact Information
    # -----------------------------------------------------

    email_columns: list[str] = field(default_factory=list)

    phone_columns: list[str] = field(default_factory=list)

    address_columns: list[str] = field(default_factory=list)

    country_columns: list[str] = field(default_factory=list)

    # -----------------------------------------------------
    # Entity Recognition
    # -----------------------------------------------------

    name_columns: list[str] = field(default_factory=list)

    company_columns: list[str] = field(default_factory=list)

    product_columns: list[str] = field(default_factory=list)

    sku_columns: list[str] = field(default_factory=list)

    barcode_columns: list[str] = field(default_factory=list)

    # -----------------------------------------------------
    # Business Semantics
    # -----------------------------------------------------

    semantic_types: dict[str, str] = field(default_factory=dict)

    # -----------------------------------------------------
    # Measurement Units
    # -----------------------------------------------------

    units: dict[str, str] = field(default_factory=dict)

    # -----------------------------------------------------
    # Currency
    # -----------------------------------------------------

    currency_columns: dict[str, str] = field(default_factory=dict)


# =========================================================
# DISCOVERY RESULT
# =========================================================

@dataclass(frozen=True)
class DiscoveryResult:
    """
    Canonical output returned by the Discovery Pipeline.

    This object is exchanged between every Discovery
    component and forms the basis for reporting,
    metadata export and downstream processing.
    """

    dataset: DatasetInfo

    basic: BasicStatistics

    schema: SchemaInfo

    numeric: NumericStatistics

    quality: QualityStatistics

    timestamp: TimestampStatistics

    column_profiles: list[ColumnProfile] = field(default_factory=list)

    inference: InferenceResult = field(default_factory=InferenceResult)

    metadata: dict[str, Any] | None = None

    report_path: str | None = None

    metadata_path: str | None = None