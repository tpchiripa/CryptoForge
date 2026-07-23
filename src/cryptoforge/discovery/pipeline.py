"""
=========================================================
CryptoForge Discovery Pipeline
=========================================================

Coordinates the entire discovery workflow.

Pipeline

Dataset Inspector
        │
        ▼
Statistics Engine
        │
        ▼
Profiling Engine
        │
        ▼
Inference Engine
        │
        ▼
Discovery Result

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


# -------------------------------------------------
# Register Inferencers
# -------------------------------------------------

import cryptoforge.discovery.inference.primary_key
import cryptoforge.discovery.inference.identifier
import cryptoforge.discovery.inference.foreign_key
import cryptoforge.discovery.inference.monotonic
import cryptoforge.discovery.inference.constant
import cryptoforge.discovery.inference.nullable
import cryptoforge.discovery.inference.categorical
import cryptoforge.discovery.inference.high_cardinality
import cryptoforge.discovery.inference.duplicate


class DiscoveryPipeline:
    """
    Coordinates the complete Discovery workflow.
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    def run(self) -> DiscoveryResult:
        """
        Execute the complete Discovery Pipeline.
        """

        self.logger.info("=" * 60)
        self.logger.info("Starting CryptoForge Discovery Pipeline")
        self.logger.info("=" * 60)

        # -------------------------------------------------
        # Dataset Inspection
        # -------------------------------------------------

        inspector = DatasetInspector()

        dataset = inspector.inspect()

        df = inspector.load_sample()

        # -------------------------------------------------
        # Statistics Engine
        # -------------------------------------------------

        statistics = StatisticsEngine(df).calculate()

        # -------------------------------------------------
        # Profiling Engine
        # -------------------------------------------------

        profiles = ProfilingEngine(df).profile()

        # -------------------------------------------------
        # Inference Engine
        # -------------------------------------------------

        inference = InferenceEngine(df).infer()

        inference_result = InferenceResult(

            primary_keys=inference.get(
                "PrimaryKeyInferencer",
                {},
            ).get(
                "primary_keys",
                [],
            ),

            identifiers=inference.get(
                "IdentifierInferencer",
                {},
            ).get(
                "identifiers",
                [],
            ),

            foreign_keys=inference.get(
                "ForeignKeyInferencer",
                {},
            ).get(
                "foreign_keys",
                [],
            ),

            categorical_columns=inference.get(
                "CategoricalInferencer",
                {},
            ).get(
                "categorical_columns",
                [],
            ),

            monotonic_columns=inference.get(
                "MonotonicInferencer",
                {},
            ).get(
                "monotonic_columns",
                [],
            ),

            constant_columns=inference.get(
                "ConstantInferencer",
                {},
            ).get(
                "constant_columns",
                [],
            ),

            nullable_columns=inference.get(
                "NullableInferencer",
                {},
            ).get(
                "nullable_columns",
                [],
            ),

            high_cardinality_columns=inference.get(
                "HighCardinalityInferencer",
                {},
            ).get(
                "high_cardinality_columns",
                [],
            ),

            duplicate_columns=inference.get(
                "DuplicateInferencer",
                {},
            ).get(
                "duplicate_columns",
                [],
            ),
        )

        # -------------------------------------------------
        # Assemble Discovery Result
        # -------------------------------------------------

        result = DiscoveryResult(

            dataset=dataset,

            basic=statistics["BasicStatisticsCalculator"],

            schema=statistics["SchemaStatisticsCalculator"],

            numeric=statistics["NumericStatisticsCalculator"],

            quality=statistics["QualityStatisticsCalculator"],

            timestamp=statistics["TimestampStatisticsCalculator"],

            column_profiles=profiles,

            inference=inference_result,
        )

        self.logger.info(
            "Discovery Pipeline completed successfully."
        )

        return result