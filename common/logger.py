import logging

from common.variables import (
    program_name,
    log_format
)


def logger_setup(
        log_name: str,
        filename: str,
        level=logging.INFO,
) -> logging.Logger:
    """
    Sets up a new logger config.

    :param log_name: Name of Logger
    :param filename: Name of Logger
    :param level: Logger level of severity
    :returns: An instance of the Logger class
    """
    # Set up formatting style
    formatter = logging.Formatter(log_format)

    handler = logging.FileHandler(filename)
    handler.setFormatter(formatter)

    # Create logger with name, level and handler
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Configure logging settings
logg_error = logger_setup(program_name, f"{program_name}_error.log")
logg_spam = logger_setup(program_name, f"{program_name}_spam.log")
