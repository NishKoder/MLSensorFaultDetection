import logging
from logging import Logger
from traceback import FrameSummary
from typing import Any, Optional, Type
import traceback
import os

from utils.constants import (
    DEFAULT_LOG_FORMAT,
    DEFAULT_DATE_FORMAT,
)


def _create_default_logger() -> logging.Logger:
    """
    Creates a default logger for exception handling.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger: Logger = logging.getLogger("AdvancedExceptionHandler")
    logger.setLevel(logging.DEBUG)

    handler: logging.StreamHandler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter: logging.Formatter = logging.Formatter(
        DEFAULT_LOG_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


class AdvancedExceptionHandler:
    """
    An advanced exception handler for Python applications.

    Features:
    - Centralized exception handling
    - Logging integration
    - Support for custom exception types
    - Type hints and docstrings for clarity
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        log_level: int = logging.ERROR
    ) -> None:
        """
        Initializes the AdvancedExceptionHandler.

        Args:
            logger (Optional[logging.Logger]): A logger instance for logging
                exceptions. If None, a default logger is created.
            log_level (int): The logging level for exceptions (default: ERROR).
        """
        self.logger: logging.Logger = logger or _create_default_logger()
        self.log_level: int = log_level

    def handle_exception(
        self,
        exc: Exception,
        custom_message: Optional[str] = None
    ) -> None:
        """
        Handles an exception by logging it and providing an optional custom message.

        Args:
            exc (Exception): The exception instance to handle.
            custom_message (Optional[str]): An optional custom message to
                include in the log.
        """
        frame: FrameSummary = traceback.extract_tb(exc.__traceback__)[-1]
        file_name: str = os.path.basename(frame.filename)
        line_number: int = frame.lineno
        if custom_message:
            self.logger.log(self.log_level, f"Custom Message: {custom_message}")
        self.logger.log(
            self.log_level,
            f"Exception occurred in file '{file_name}', "
            f"line {line_number}: {str(exc)}"
        )

    def raise_custom_exception(
        self,
        exception_type: Type[Exception],
        message: str
    ) -> None:
        """
        Raises a custom exception with the specified type and message.

        Args:
            exception_type (Type[Exception]): The type of exception to raise.
            message (str): The message for the exception.
        """
        self.logger.log(
            self.log_level,
            f"Raising exception: {exception_type.__name__} - {message}"
        )
        raise exception_type(message)

    def validate_input(
        self,
        value: Any,
        expected_type: Type[Any],
        field_name: str
    ) -> None:
        """
        Validates the input type and raises a ValueError if the type is incorrect.

        Args:
            value (Any): The value to validate.
            expected_type (Type[Any]): The expected type of the value.
            field_name (str): The name of the field being validated
                (used for logging and error messages).

        Raises:
            ValueError: If the value does not match the expected type.
        """
        if not isinstance(value, expected_type):
            error_message: str = (
                f"Invalid type for field '{field_name}': "
                f"Expected {expected_type.__name__}, "
                f"got {type(value).__name__}."
            )
            self.logger.log(self.log_level, error_message)
            raise ValueError(error_message)
        self.logger.debug(
            f"Validation successful for field '{field_name}' with value: {value}"
        )
