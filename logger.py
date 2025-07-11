"""
Logging module for OBS Utils
Provides consistent logging configuration
"""

import logging
import os
from datetime import datetime
from typing import Optional


def setup_logger(name: str = __name__, log_level: str = "INFO", log_dir: str = "logs") -> logging.Logger:
    """
    Setup logger with file and console handlers

    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_dir: Directory for log files

    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create formatters
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")

    # File handler
    dt_now = datetime.now()
    log_file = os.path.join(log_dir, f"obs_utils_{dt_now.strftime('%Y-%m-%d_%H-%M-%S')}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """Get existing logger or create new one"""
    return logging.getLogger(name) if logging.getLogger(name).handlers else setup_logger(name)
