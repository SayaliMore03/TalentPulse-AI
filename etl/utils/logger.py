import logging
from logging import Logger
from pathlib import Path

def get_logger(name: str) -> Logger:
    """
    Creates and returns a configured logger.

    Logs are written to:
    - Console
    - logs/etl.log
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(log_dir / "etl.log", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.propagate = False

    return logger