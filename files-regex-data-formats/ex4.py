import re

def redact_sensitive_data(content: str) -> str:
    """
    Finds and redacts sensitive values (api_key, password, secret) in a string.

    Args:
        content (str): The string content to be sanitized.

    Returns:
        str: The content with sensitive values replaced by '[REDACTED]', only the value part of the line, leaving the key and the separator intact
    
    Raises:
        TypeError: If content is not a string.
    """
    # Input validation
    if not isinstance(content, str):
        raise TypeError(f"Content must be string, got {type(content).__name__!r}")
    
    # Regex pattern:
    # (?i)                    → case-insensitive (matches Password, PASSWORD, etc.)
    # (?<!\w)                 → lookbehind: not preceded by a word character
    # (api_key|password|secret) → capture group 1: the sensitive key name
    # (\s*[=:]\s*)              → capture group 2: the separator (colon or equals sign) with its surrounding spaces preserved
    # (".*?"|'.*?'|\S+)       → capture group 3: the value — quoted string OR unquoted word
    sensitive_pattern = r"(?i)(?<!\w)(api_key|password|secret)(\s*[=:]\s*)(\".*?\"|'.*?'|\S+)"

    # \1 and \2 put the key and separator back; only the value becomes [REDACTED]
    updated_content = re.sub(sensitive_pattern, r"\1\2[REDACTED]", content)
    # Return the redacted content.
    return updated_content
    

file_content = 'api_key = "abc-123"\nPassword: secret'
redacted_content = redact_sensitive_data(file_content)
print(redacted_content)