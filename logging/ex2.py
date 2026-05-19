import logging
import logging.handlers
import sys


def configure_rotating_logger(
    logger_name: str,
    log_filepath: str,
    max_size_bytes: int,
    backup_count: int,
) -> logging.Logger:
    """
    Configures and returns a logger that writes to a rotating file.

    Args:
        logger_name (str): The name for the logger.
        log_filepath (str): The path to the log file.
        max_size_bytes (int): Max file size in bytes before rotation.
        backup_count (int): Number of backup files to keep.

    Returns:
        logging.Logger: A fully configured rotating logger.

    Raises:
        TypeError: If any argument has the wrong type.
        ValueError: If any argument has an invalid value.
    """
    # --- Input validation ---
    for param_name, value in (("logger_name", logger_name), ("log_filepath", log_filepath)):
        if not isinstance(value, str):
            raise TypeError(f"{param_name} must be a string, got {type(value).__name__!r}")
        if not value.strip():
            raise ValueError(f"{param_name} must be a non-empty string")

    for param_name, value in (("max_size_bytes", max_size_bytes), ("backup_count", backup_count)):
        # Without bool guard, backup_count=True would silently pass validation
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{param_name} must be an integer, got {type(value).__name__!r}")

    if max_size_bytes <= 0:
        raise ValueError(f"max_size_bytes must be greater than 0, got {max_size_bytes}")
    if backup_count < 0:
        raise ValueError(f"backup_count must be a non-negative integer, got {backup_count}")

    # --- Logger setup ---
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    rotating_fh = logging.handlers.RotatingFileHandler(
        log_filepath,
        maxBytes=max_size_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    rotating_fh.setLevel(logging.DEBUG)

    logger.addHandler(rotating_fh)

    return logger


# Configure a logger that rotates after ~1KB and keeps 3 backups.
log_path = "monitor_service.log"
service_logger = configure_rotating_logger(
    logger_name="monitoring_service",
    log_filepath=log_path,
    max_size_bytes=1024,
    backup_count=3,
)

for i in range(200):
    service_logger.info(f"Checking status of component {i}.")