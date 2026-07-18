"""
=========================================================
CryptoForge Discovery Contracts
=========================================================

Shared dataclasses used throughout the Discovery module.

Author: Tichaona Peter Chiripa
=========================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


# =========================================================
# Dataset Information
# =========================================================

@dataclass(slots=True)
class DatasetInfo:
    zip_file: str
    csv_file: str
    zip_size_bytes: int
    csv_size_bytes: int
    compression_ratio_percent: float


# =========================================================
# Sample Statistics
# =========================================================

@dataclass(slots=True)
class SampleStatistics:
    sample_rows: int
    column_count: int
    missing_values: int
    duplicate_rows: int
    memory_bytes: int


# =========================================================
# Schema Information
# =========================================================

@dataclass(slots=True)
class SchemaInfo:
    columns: List[str]
    dtypes: Dict[str, str]


# =========================================================
# Numeric Statistics
# =========================================================

@dataclass(slots=True)
class NumericStatistics:
    summary: Dict[str, Any] = field(default_factory=dict)


# =========================================================
# Discovery Result
# =========================================================

@dataclass(slots=True)
class DiscoveryResult:
    dataset: DatasetInfo
    statistics: SampleStatistics
    schema: SchemaInfo
    numeric: NumericStatistics
