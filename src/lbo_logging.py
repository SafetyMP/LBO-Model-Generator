"""
Logging configuration for LBO Model Generator.
Provides structured logging with configurable levels and handlers.
"""

import logging
import logging.config
import os
from typing import Optional, Dict, Any, List


def _get_log_level(log_level: Optional[str] = None) -> str:
    """Get and validate log level."""
    if log_level is None:
        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if log_level not in valid_levels:
        log_level = "INFO"

    return log_level


def _get_formatters() -> Dict[str, Any]:
    """Get logging formatters configuration."""
    return {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s", "datefmt": "%Y-%m-%d %H:%M:%S"},
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }


def _get_console_handler(log_level: str) -> Dict[str, Any]:
    """Get console handler configuration."""
    return {"level": log_level, "formatter": "standard", "class": "logging.StreamHandler", "stream": "ext://sys.stdout"}


def _get_file_handler(log_level: str, log_file: str) -> Dict[str, Any]:
    """Get file handler configuration."""
    return {
        "level": log_level,
        "formatter": "detailed",
        "class": "logging.FileHandler",
        "filename": log_file,
        "mode": "a",
        "encoding": "utf-8",
    }


def _get_loggers(handlers: List[str], log_level: str) -> Dict[str, Any]:
    """Get loggers configuration."""
    logger_names = ["", "lbo_model_generator", "lbo_ai_recommender", "lbo_ai_validator", "lbo_industry_excel"]

    return {name: {"handlers": handlers, "level": log_level, "propagate": False} for name in logger_names}


def get_logging_config(log_level: Optional[str] = None, log_file: Optional[str] = None) -> Dict[str, Any]:
    """Get logging configuration dictionary.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   If None, uses environment variable LOG_LEVEL or defaults to INFO.
        log_file: Optional path to log file. If None, only logs to console.

    Returns:
        Logging configuration dictionary compatible with logging.config.dictConfig()
    """
    log_level = _get_log_level(log_level)
    handlers = ["console"]

    if log_file:
        handlers.append("file")

    config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": _get_formatters(),
        "handlers": {
            "console": _get_console_handler(log_level),
        },
        "loggers": _get_loggers(handlers, log_level),
    }

    if log_file:
        config["handlers"]["file"] = _get_file_handler(log_level, log_file)

    return config


def setup_logging(log_level: Optional[str] = None, log_file: Optional[str] = None) -> None:
    """Configure logging for the LBO Model Generator.

    This function sets up structured logging with configurable levels.
    It should be called once at application startup.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   If None, uses environment variable LOG_LEVEL or defaults to INFO.
        log_file: Optional path to log file. If provided, logs will also be written to this file.

    Example:
        >>> setup_logging(log_level='DEBUG', log_file='lbo_model.log')
        >>> logger = logging.getLogger(__name__)
        >>> logger.info("Logging configured")
    """
    config = get_logging_config(log_level=log_level, log_file=log_file)
    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


# Initialize logging with default configuration on import
# Users can override by calling setup_logging() with different parameters
_log_level = os.environ.get("LOG_LEVEL", "INFO")
_log_file = os.environ.get("LOG_FILE", None)
setup_logging(log_level=_log_level, log_file=_log_file)
