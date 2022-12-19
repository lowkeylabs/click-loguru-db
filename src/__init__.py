#
import sys
from loguru import logger
DEFAULT_LOG_LEVEL="TRACE"

logger.remove()
logger.add(sys.stderr, level=DEFAULT_LOG_LEVEL)

logger.trace(f"Inside {__file__}")
