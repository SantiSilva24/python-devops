import re
from typing import Optional

def parse_login_event(log_line: str) -> Optional[dict[str, str]]:
    """
    Parses a login event log line to extract the username and status.

    Args:
        log_line (str): The log line to parse.

    Returns:
        A dictionary with 'username' and 'status' if the line matches,
        otherwise None.
        
    Raises:
        TypeError: If log_line is not a string.
    """
    # Input validation
    if not isinstance(log_line, str):
        raise TypeError(f"Log line must be string, got {type(log_line).__name__!r}")
    
    # Parse the following string format: "LOGIN_EVENT: User '{username}' login attempt was {status}."
    
    # LOGIN_EVENT:\s+  → matches the literal prefix "LOGIN_EVENT:" and any following spaces
    # User\s+          → matches "User" and the space after it
    # '(?P<username>   → opening quote, then starts a named capture group called 'username'
    # \w+)'            → one or more word characters (the username), then closing quote
    # \s+login\s+attempt\s+was\s+  → matches the fixed middle text with flexible spacing
    # (?P<status>      → starts a named capture group called 'status'
    # \w+)             → one or more word characters (the status value)
    # \.               → matches the literal period at the end
    login_pattern = r"LOGIN_EVENT:\s+User\s+'(?P<username>\w+)'\s+login\s+attempt\s+was\s+(?P<status>\w+)\."
    
    # If a match is found, return the dictionary of named groups; otherwise, return None.
    match = re.search(login_pattern, log_line)
    if not match:
        return None
    return match.groupdict()

log1 = "LOGIN_EVENT: User 'jdoe' login attempt was SUCCESSFUL."
log2 = "LOGIN_EVENT: User 'admin' login attempt was FAILED."
log3 = "INFO: Application started."
 
print(parse_login_event(log1))  # Expected: {'username': 'jdoe', 'status': 'SUCCESSFUL'}
print(parse_login_event(log2))  # Expected: {'username': 'admin', 'status': 'FAILED'}
print(parse_login_event(log3))  # Expected: None
