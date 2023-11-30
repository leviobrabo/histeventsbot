from loguru import logger

from .config import LOG_PATH

logger.add(LOG_PATH)
