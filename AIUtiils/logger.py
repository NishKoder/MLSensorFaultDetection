import os
import sys
import datetime
import logging
import logging.handlers
from typing import Optional

from AIUtiils.constants import (
    MAX_LOG_FILE_SIZE,
    BACKUP_LOG_COUNT,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_DIR,
    DEFAULT_DATE_FORMAT,
)
from AIUtiils.types import UnionDT


class AdvancedMLLogger:
    """
    A robust, advanced, and optimized logger for Machine Learning applications.

    Features:
    - Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    - File and console output with customizable formats.
    - Rotating file handler to manage log file size.
    - Exception handling and traceback logging.
    - Type hinting for improved code clarity.
    - Optional custom formatting for specific data types.

    """

    def __init__(
        self,
        name: str = "Logs",
        log_dir: str = DEFAULT_LOG_DIR,
        max_bytes: int = MAX_LOG_FILE_SIZE,
        backup_count: int = BACKUP_LOG_COUNT,
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        custom_formatters: Optional[dict] = None
    ) -> None:
        """
        Initializes the AdvancedMLLogger.

        Args:
            name: The name of the logger (e.g., the name of your ML module).
            log_dir: The directory where log files will be stored.
            max_bytes: Maximum size of a log file before rotation (default: 10 MB).
            backup_count: Number of backup log files to keep (default: 5).
            console_level: Logging level for console output (default: INFO).
            file_level: Logging level for file output (default: DEBUG).
            custom_formatters: Optional dictionary to specify custom formatters
                for specific data types.
        """

        self.name: str = name
        self.log_dir: str = log_dir
        self.max_bytes: int = max_bytes
        self.backup_count: int = backup_count
        self.console_level: int = console_level
        self.file_level: int = file_level

        os.makedirs(self.log_dir, exist_ok=True)

        self.logger: logging.Logger = logging.getLogger(self.name)
        if not self.logger.hasHandlers():  # Check if handlers already exist
            self.logger.setLevel(logging.DEBUG)

            base_formatter: logging.Formatter = logging.Formatter(
                DEFAULT_LOG_FORMAT,
                datefmt=DEFAULT_DATE_FORMAT
            )
            if custom_formatters:
                class CustomFormatter(logging.Formatter):
                    def format(self, record):
                        for data_type, formatter_func in custom_formatters.items():
                            if isinstance(record.msg, data_type):
                                record.msg = formatter_func(record.msg)
                        return super().format(record)
                base_formatter = CustomFormatter(
                    DEFAULT_LOG_FORMAT,
                    datefmt=DEFAULT_DATE_FORMAT
                )

            console_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.console_level)
            console_handler.setFormatter(base_formatter)
            self.logger.addHandler(console_handler)

            timestamp: str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file_path: str = os.path.join(
                self.log_dir, f"{self.name}_{timestamp}.log"
            )
            file_handler: logging.handlers.RotatingFileHandler = (
                logging.handlers.RotatingFileHandler(
                    log_file_path,
                    maxBytes=self.max_bytes,
                    backupCount=self.backup_count
                )
            )
            file_handler.setLevel(self.file_level)
            file_handler.setFormatter(base_formatter)
            self.logger.addHandler(file_handler)

    def debug(self, msg: UnionDT, *args, **kwargs) -> None:
        """Logs a debug message."""
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: UnionDT, *args, **kwargs) -> None:
        """Logs an info message."""
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: UnionDT, *args, **kwargs) -> None:
        """Logs a warning message."""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: UnionDT, *args, **kwargs) -> None:
        """Logs an error message."""
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: UnionDT, *args, **kwargs) -> None:
        """Logs a critical message."""
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg: UnionDT, *args, **kwargs) -> None:
        """Logs an exception with traceback."""
        self.logger.exception(msg, *args, **kwargs)