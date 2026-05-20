import re

def has_critical_error(log_line: str) -> bool:
    """
    Checks if a log line contains a critical error indicator ('ERROR:' or 'FAIL:').
    The check is case-insensitive.

    Args:
        log_line (str): The log line to check.

    Returns:
        bool: True if a critical error indicator is found, False otherwise.
    """
    
    # (?<!\w)      → lookbehind: only match if NOT preceded by a word character (letter/digit/_)
    #                this prevents matching if ERROR/FAIL is in the middle of a word
    # (ERROR|FAIL) → match either literal string "ERROR" or "FAIL"
    # :            → must be immediately followed by a colon
    # (?!\w)       → lookahead: only match if NOT followed by a word character
    #                this prevents matching things like "FAIL:ure"
    error_pattern = r"(?<!\w)(ERROR|FAIL):(?!\w)"

    return bool(re.search(error_pattern, log_line, re.IGNORECASE))
    


line1 = "2023-10-27 INFO: System started successfully."
line2 = "2023-10-27 ERROR: Database connection lost."
line3 = "2023-10-27 WARN: Disk usage high, but operation will not fail, all clear." # fail is present but followed by a comma
line4 = "2023-10-27 DEBUG: User 'test' initiated a fail: sequence." # "fail:" is present
 
print(has_critical_error(line1))  # Expected: False
print(has_critical_error(line2))  # Expected: True
print(has_critical_error(line3))  # Expected: False
print(has_critical_error(line4))  # Expected: True