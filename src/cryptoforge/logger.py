"""
Global application logger.
"""

from cryptoforge.core.logging import (
    configure_logging,
    get_logger,
)

configure_logging()

logger = get_logger(__name__)