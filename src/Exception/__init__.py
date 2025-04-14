import sys
import logging

def error_message_detail(error: Exception, error_detail: sys, logger: logging.Logger = None) -> str:
    """
    Extracts detailed error information including file name, line number, and the error message.

    :param error: The exception that occurred.
    :param error_detail: The sys module (used to access traceback info).
    :param logger: Optional custom logger to log the error. Falls back to root logger if None.
    :return: A formatted error message string.
    """

    # Unpack the traceback object using exc_info()
    # exc_tb contains the traceback details
    _, _, exc_tb = error_detail.exc_info()

    # Get the filename where the exception occurred
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Get the exact line number in the file where the error occurred
    line_number = exc_tb.tb_lineno

    # Format the error message including filename, line, and exception message
    error_message = f"Error occurred in script: [{file_name}] at line [{line_number}]: {str(error)}"

    # If a custom logger is provided, use it; else fallback to default root logger
    if logger:
        logger.error(error_message)
    else:
        logging.error(error_message)

    return error_message


class MyException(Exception):
    """
    Custom exception class that logs detailed error info using error_message_detail().
    Can be used throughout the project to wrap any unexpected exceptions.
    """
    def __init__(self, error_message: str, error_detail: sys, logger: logging.Logger = None):
        """
        Constructor for MyException.

        :param error_message: The original error message you want to describe.
        :param error_detail: The sys module passed to extract traceback info.
        :param logger: Optional logger instance to record the error log.
        """
        # Initialize the base Exception class with the original error message
        super().__init__(error_message)

        # Get the full error details including file name and line number
        # and log it using the logger if provided
        self.error_message = error_message_detail(error_message, error_detail, logger=logger)

    def __str__(self) -> str:
        """
        Override the __str__ method so the exception prints the full error message
        """
        return self.error_message
