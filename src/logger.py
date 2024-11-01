import logging
from typing import Optional
import os
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output."""

    COLORS = {
        'DEBUG': '\033[0;36m',  # Cyan
        'INFO': '\033[0;32m',  # Green
        'WARNING': '\033[0;33m',  # Yellow
        'ERROR': '\033[0;31m',  # Red
        'CRITICAL': '\033[0;35m',  # Purple
        'RESET': '\033[0m'
    }

    def format(self, record):
        if hasattr(record, 'color'):
            return record.color + super().format(record) + self.COLORS['RESET']

        record.color = self.COLORS.get(record.levelname, '')
        return record.color + super().format(record) + self.COLORS['RESET']


def setup_logger(
        name: str,
        log_file: Optional[str] = None,
        level: str = "INFO"
) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    # Console handler with colored output
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        try:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to setup file handler: {e}")

    return logger


class LoggerWrapper:
    """Wrapper for adding context to logs."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.context = {}

    def add_context(self, **kwargs):
        """Add context to logs."""
        self.context.update(kwargs)

    def format_message(self, message: str) -> str:
        """Format message with context."""
        if self.context:
            context_str = ' '.join(f'{k}={v}' for k, v in self.context.items())
            return f"{message} [{context_str}]"
        return message

    def debug(self, message: str, **kwargs):
        """Log debug message with context."""
        self.add_context(**kwargs)
        self.logger.debug(self.format_message(message))

    def info(self, message: str, **kwargs):
        """Log info message with context."""
        self.add_context(**kwargs)
        self.logger.info(self.format_message(message))

    def warning(self, message: str, **kwargs):
        """Log warning message with context."""
        self.add_context(**kwargs)
        self.logger.warning(self.format_message(message))

    def error(self, message: str, **kwargs):
        """Log error message with context."""
        self.add_context(**kwargs)
        self.logger.error(self.format_message(message))

    def critical(self, message: str, **kwargs):
        """Log critical message with context."""
        self.add_context(**kwargs)
        self.logger.critical(self.format_message(message))