import logging
from logging.handlers import RotatingFileHandler
import os
from from_root import from_root
from datetime import datetime
from colorlog import ColoredFormatter
from src.Constants.global_logging import LOG_SESSION_TIME

LOG_DIR = 'logs'
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

def configure_logger(logger_name: str, level: str = "INFO", to_console: bool = True, to_file: bool = True, log_file_name: str = None) -> logging.Logger:
    """
    Configure Logger with optional Console and Rotating File Handlers.
    :param logger_name: Logger name (e.g., __name__)
    :param level: Logging level ('DEBUG', 'INFO', etc.)
    :param to_console: Enable console logging
    :param to_file: Enable file logging
    :param log_file_name: If provided, it will be used for log file, else default timestamped file name will be used
    :return: Configured logger instance
    """
    
    # Define log directory path
    log_dir_path = os.path.join(from_root(), LOG_DIR,LOG_SESSION_TIME)
    os.makedirs(log_dir_path, exist_ok=True)

    # Create logger
    logger = logging.getLogger(logger_name)

    # Prevent duplicate handlers on multiple logger configurations
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set logger level
    level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(level)

    # Define log formatter with colored output
    formatter = ColoredFormatter(
    "%(log_color)s %(asctime)s - %(name)s - %(levelname)s - %(message)s ",  # Added space after %(log_color)s
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red"
    }
)

    
    # Console logging configuration
    if to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File logging configuration
    if to_file:
        # Generate log file name if not provided
        if log_file_name is None:
            log_file_name = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}"
        
        log_file_path = os.path.join(log_dir_path,f"{log_file_name}.log")
        file_handler = RotatingFileHandler(
            filename=log_file_path,
            encoding="utf-8",
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Optional: Prevent duplication with root logger
    logger.propagate = False
    return logger
