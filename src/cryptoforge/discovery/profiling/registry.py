"""
=========================================================
CryptoForge Profiling Registry
=========================================================

Registers all available profilers.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations


class ProfilingRegistry:
    """
    Registry of profiling components.
    """

    _profilers = []

    @classmethod
    def register(cls, profiler):
        cls._profilers.append(profiler)
        return profiler

    @classmethod
    def count(cls):
        return len(cls._profilers)

    @classmethod
    def all(cls):
        """
        Return all registered profilers.
        """
        return cls._profilers.copy()