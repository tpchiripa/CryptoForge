"""
=========================================================
CryptoForge Resource Paths
=========================================================

Resolves knowledge-base CSV paths relative to the installed
package location, not the current working directory.

Every inferencer that loads a dictionary (country.py, name.py,
company.py, product.py, ...) was previously hardcoding a path like:

    "src/cryptoforge/discovery/resources/datasets/countries.csv"

That string only resolves correctly if the process happens to be
launched from the repo root. It silently returns an empty dictionary
(no error) if launched from anywhere else -- a test runner, Airflow,
another machine. dataset_path() below fixes that by resolving against
this file's own location on disk, which is stable regardless of cwd.

Author:
    Tichaona Peter Chiripa
=========================================================
"""

from __future__ import annotations

from pathlib import Path

# This file lives at src/cryptoforge/discovery/resources/paths.py, so
# its own parent directory *is* the resources/ folder.
_RESOURCES_DIR = Path(__file__).resolve().parent
DATASETS_DIR = _RESOURCES_DIR / "datasets"
KNOWLEDGE_DIR = _RESOURCES_DIR / "knowledge"


def dataset_path(filename: str) -> str:
    """
    Absolute path to a file under resources/datasets/, e.g.
    dataset_path("countries.csv") -> resources/datasets/countries.csv
    regardless of what directory the process was launched from.
    """
    return str(DATASETS_DIR / filename)


def knowledge_path(*parts: str) -> str:
    """
    Absolute path to a file under resources/knowledge/<subfolder>/, e.g.
    knowledge_path("countries", "countries.csv").
    Not used yet -- resources/datasets/ is the live tree as of this
    session -- but kept available for when/if resources/knowledge/ gets
    consolidated in or retired.
    """
    return str(KNOWLEDGE_DIR.joinpath(*parts))
