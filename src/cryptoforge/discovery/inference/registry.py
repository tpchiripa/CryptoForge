"""
=========================================================
CryptoForge Inference Registry
=========================================================

Automatically registers every metadata inferencer.

The Inference Engine executes inferencers in the
order they are registered.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from typing import Type

from cryptoforge.discovery.inference.base import BaseInferencer


class InferenceRegistry:
    """
    Registry of all metadata inferencers.
    """

    _inferencers: list[Type[BaseInferencer]] = []

    @classmethod
    def register(cls, inferencer: Type[BaseInferencer]):
        """
        Register a metadata inferencer.
        """

        if inferencer not in cls._inferencers:
            cls._inferencers.append(inferencer)

        return inferencer

    @classmethod
    def inferencers(cls) -> list[Type[BaseInferencer]]:
        """
        Return all registered inferencers.
        """

        return cls._inferencers

    @classmethod
    def count(cls) -> int:
        """
        Number of registered inferencers.
        """

        return len(cls._inferencers)

    @classmethod
    def clear(cls):
        """
        Remove every registered inferencer.

        Mainly used by unit tests.
        """

        cls._inferencers.clear()

    @classmethod
    def names(cls) -> list[str]:
        """
        Return inferencer class names.
        """

        return [
            inferencer.__name__
            for inferencer in cls._inferencers
        ]


# =========================================================
# Convenience Decorator
# =========================================================

# Allows inferencers to simply use:
#
#     from cryptoforge.discovery.inference.registry import register
#
#     @register
#     class MyInferencer(BaseInferencer):
#         ...
#
register = InferenceRegistry.register