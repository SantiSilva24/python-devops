def parse_log_line(log_line: str) -> dict | None:
    """
    Parses a single log line into a structured dictionary.

    The expected log format is: "TIMESTAMP [LOG_LEVEL] MESSAGE"
    Example: "2024-05-20T13:45:10Z [INFO] User 'alice' logged in successfully."

    Args:
        log_line: A string representing a single line from a log file.

    Returns:
        A dictionary containing the 'timestamp', 'log_level', and 'message'
        if the log line is valid, otherwise None.
    """
    if not isinstance(log_line, str) or not log_line.strip():
        print("The log must not be empty")
        return None
    
    # Split only the first 2 spaces
    parts = log_line.split(" ", 2)
    
    # The involved parts should be 3
    if not len(parts) == 3:
        return None
    timestamp, log_level, message = parts
    
    # Validate log level format
    if not (log_level.startswith("[") and log_level.endswith("]")):
        return None

    # Remove brackets
    log_level = log_level.strip('[]')

    return {
        "timestamp": timestamp,
        "log_level": log_level,
        "message": message
    }
    
log = "2024-05-20T14:00:05Z [ERROR] Failed to connect to database."
    
print(parse_log_line(log))
