from cryptoforge.core.logging import (
    configure_logging,
    get_logger,
)

configure_logging()

logger = get_logger(__name__)

logger.info("CryptoForge started.")
logger.info("Reading configuration...")
logger.warning("This is only a warning.")
logger.error("This is a simulated error.")
logger.info("Logging test complete.")
