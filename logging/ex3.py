import logging
import logging.config
import json
from typing import Any, Dict


def configure_logging(verbose: bool) -> logging.Logger:
    """
    Configures logging dynamically based on a verbose flag.

    Args:
        verbose (bool): If True, sets the root logger level to DEBUG.
                        Otherwise, the level remains INFO.

    Returns:
        logging.Logger: The configured root logger instance.

    Raises:
        TypeError: If verbose is not a boolean.
    """
    if not isinstance(verbose, bool):
        raise TypeError(f"Verbose must be boolean, got {type(verbose).__name__!r}")

    base_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": True,
        "handlers": {},
        "formatters": {},
        "loggers": {},
    }

    base_config["formatters"]["simple"] = {
        "format": "%(levelname)s: %(message)s"
    }

    base_config["handlers"]["console"] = {
        "class": "logging.StreamHandler",
        "level": "DEBUG",
        "formatter": "simple",
        "stream": "ext://sys.stdout",
    }

    base_config["root"] = {
        "level": "INFO",
        "handlers": ["console"],
    }

    if verbose:
        base_config["root"]["level"] = "DEBUG"

    logging.config.dictConfig(base_config)

    return logging.getLogger()



