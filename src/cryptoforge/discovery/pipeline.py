"""
=========================================================
CryptoForge Discovery Pipeline
=========================================================

Coordinates the complete Discovery workflow.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from cryptoforge.logger import get_logger

from cryptoforge.discovery.contracts import (
    DiscoveryResult,
    InferenceResult,
)

from cryptoforge.discovery.inspector import DatasetInspector
from cryptoforge.discovery.statistics.engine import StatisticsEngine
from cryptoforge.discovery.profiling.engine import ProfilingEngine
from cryptoforge.discovery.inference.engine import InferenceEngine


# =========================================================
# Register Inferencers
# =========================================================

import cryptoforge.discovery.inference.primary_key
import cryptoforge.discovery.inference.identifier
import cryptoforge.discovery.inference.business_key
import cryptoforge.discovery.inference.foreign_key
import cryptoforge.discovery.inference.monotonic
import cryptoforge.discovery.inference.constant
import cryptoforge.discovery.inference.nullable
import cryptoforge.discovery.inference.categorical
import cryptoforge.discovery.inference.high_cardinality
import cryptoforge.discovery.inference.duplicate
import cryptoforge.discovery.inference.pii
import cryptoforge.discovery.inference.semantic_type
import cryptoforge.discovery.inference.units
import cryptoforge.discovery.inference.currency
import cryptoforge.discovery.inference.email


class DiscoveryPipeline:
    """
    Coordinates the complete Discovery workflow.
    """

    def __init__(self) -> None:
        self.logger = get_logger(__name__)

    def run(self) -> DiscoveryResult:

        self.logger.info("=" * 60)
        self.logger.info("Starting CryptoForge Discovery Pipeline")
        self.logger.info("=" * 60)

        # =====================================================
        # Dataset Inspection
        # =====================================================

        inspector = DatasetInspector()

        dataset = inspector.inspect()

        df = inspector.load_sample()

        # =====================================================
        # Statistics
        # =====================================================

        statistics = StatisticsEngine(df).calculate()

        # =====================================================
        # Profiling
        # =====================================================

        profiles = ProfilingEngine(df).profile()

        # =====================================================
        # Inference
        # =====================================================

        inference = InferenceEngine(df).infer()

        inference_result = InferenceResult(

            # -------------------------------------------------
            # Keys
            # -------------------------------------------------

            primary_keys=inference.get(
                "PrimaryKeyInferencer", {}
            ).get(
                "primary_keys", []
            ),

            identifiers=inference.get(
                "IdentifierInferencer", {}
            ).get(
                "identifiers", []
            ),

            business_keys=inference.get(
                "BusinessKeyInferencer", {}
            ).get(
                "business_keys", []
            ),

            foreign_keys=inference.get(
                "ForeignKeyInferencer", {}
            ).get(
                "foreign_keys", []
            ),

            # -------------------------------------------------
            # Structural Metadata
            # -------------------------------------------------

            categorical_columns=inference.get(
                "CategoricalInferencer", {}
            ).get(
                "categorical_columns", []
            ),

            monotonic_columns=inference.get(
                "MonotonicInferencer", {}
            ).get(
                "monotonic_columns", []
            ),

            constant_columns=inference.get(
                "ConstantInferencer", {}
            ).get(
                "constant_columns", []
            ),

            nullable_columns=inference.get(
                "NullableInferencer", {}
            ).get(
                "nullable_columns", []
            ),

            high_cardinality_columns=inference.get(
                "HighCardinalityInferencer", {}
            ).get(
                "high_cardinality_columns", []
            ),

            duplicate_columns=inference.get(
                "DuplicateInferencer", {}
            ).get(
                "duplicate_columns", []
            ),

            # -------------------------------------------------
            # Governance
            # -------------------------------------------------

            pii_columns=inference.get(
                "PIIInferencer", {}
            ).get(
                "pii_columns", []
            ),

            # -------------------------------------------------
            # Business Metadata
            # -------------------------------------------------

            semantic_types=inference.get(
                "SemanticTypeInferencer", {}
            ).get(
                "semantic_types", {}
            ),

            units=inference.get(
                "UnitsInferencer", {}
            ).get(
                "units", {}
            ),

            # -------------------------------------------------
            # Currency Metadata
            # -------------------------------------------------

            currency_columns=inference.get(
                "CurrencyInferencer", {}
            ).get(
                "currency_columns", {}
            ),
        )

        # =====================================================
        # Assemble Discovery Result
        # =====================================================

        result = DiscoveryResult(

            dataset=dataset,

            basic=statistics[
                "BasicStatisticsCalculator"
            ],

            schema=statistics[
                "SchemaStatisticsCalculator"
            ],

            numeric=statistics[
                "NumericStatisticsCalculator"
            ],

            quality=statistics[
                "QualityStatisticsCalculator"
            ],

            timestamp=statistics[
                "TimestampStatisticsCalculator"
            ],

            column_profiles=profiles,

            inference=inference_result,
        )

        self.logger.info(
            "Discovery Pipeline completed successfully."
        )

        return result          