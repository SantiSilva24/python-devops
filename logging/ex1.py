import logging
import sys

def setup_script_logger(logger_name):
    """
    Configures and returns a logger for script activity monitoring.

    Args:
        logger_name (str): The name for the logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    if not isinstance(logger_name, str):
        raise TypeError("The logger name must be a string")
    if not logger_name.strip():
        raise ValueError("The logger name must be non-empty")
    
    # Get a logger instance with the specified base level = INFO        
    baked_logger = logging.getLogger(logger_name)
    baked_logger.setLevel(logging.INFO)
    
    # Clear any existing handlers before adding a new one
    baked_logger.handlers.clear()
    
    # Set up handler for stdout
    stream_handler = logging.StreamHandler(sys.stdout)

    # Set up formatter with <TIMESTAMP> - <LEVEL> - <MESSAGE>
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Link formatter to handler
    stream_handler.setFormatter(formatter)
    
    baked_logger.addHandler(stream_handler)
    
    return baked_logger
    
    
script_logger = setup_script_logger('deployment_script')
 
script_logger.debug("This is a debug message. It will not appear.")
script_logger.info("Starting deployment to production.")
script_logger.warning("Network latency is high.")