"""
=========================================================
CryptoForge Inferencer Auto Loader
=========================================================

Automatically imports every inferencer module so that
each inferencer registers itself with the registry.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

import importlib
import pkgutil

import cryptoforge.discovery.inference as package

EXCLUDED_MODULES = {
    "__init__",
    "autoload",
    "base",
    "engine",
    "registry",
}

for _, module_name, _ in pkgutil.iter_modules(package.__path__):

    if module_name in EXCLUDED_MODULES:
        continue

    importlib.import_module(
        f"{package.__name__}.{module_name}"
    )