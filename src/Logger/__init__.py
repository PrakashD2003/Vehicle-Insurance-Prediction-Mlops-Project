import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from colorlog import ColoredFormatter
from src.Constants.global_logging import LOG_SESSION_TIME

LOG_DIR = "logs"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

def configure_logger(
    logger_name: str,
    level: str = "INFO",
    to_console: bool = True,
    to_file: bool = True,
    log_file_name: str = None
) -> logging.Logger:
    """
    Configure a logger with optional console and rotating file handlers.

    :param logger_name: Name of the logger (e.g., __name__)
    :param level: Logging level ('DEBUG', 'INFO', etc.)
    :param to_console: Enable console logging
    :param to_file: Enable file logging
    :param log_file_name: Custom log file name (defaults to timestamp)
    :return: Configured Logger instance
    """
    # Determine project root (2 levels up: src/Logger -> src -> project root)
    base_dir = Path(__file__).resolve().parents[2]
    log_dir_path = base_dir / LOG_DIR / LOG_SESSION_TIME
    log_dir_path.mkdir(parents=True, exist_ok=True)

    # Create or retrieve the logger
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set logging level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Define colored log formatter
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red"
        }
    )

    # Console handler
    if to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if to_file:
        if log_file_name is None:
            log_file_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        log_file_path = log_dir_path / f"{log_file_name}.log"
        file_handler = RotatingFileHandler(
            filename=str(log_file_path),
            encoding="utf-8",
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent log propagation to root logger
    logger.propagate = False
    return logger
