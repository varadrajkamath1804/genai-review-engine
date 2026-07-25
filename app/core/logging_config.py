import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.core.config import get_settings

settings = get_settings()


def configure_logging() -> None:
    logs_directory = Path(settings.LOG_FILE).parent
    logs_directory.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(settings.LOG_LEVEL)
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )

    file_handler.setLevel(settings.LOG_LEVEL)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    logger.addHandler(stream_handler)
    if settings.LOG_TO_FILE:
        logger.addHandler(file_handler)
