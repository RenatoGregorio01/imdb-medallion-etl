from pathlib import Path

from loguru import logger

LOGS_PATH = Path("logs")
LOGS_PATH.mkdir(exist_ok=True)

logger.add(
    LOGS_PATH / "pipeline.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    format=("{time:YYYY-MM-DD HH:mm:ss} | " "{level} | " "{message}"),
)

__all__ = ["logger"]
