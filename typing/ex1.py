from typing import Any

# Add type hints to the function signature below.
# - service_name should be a string (str).
# - port should be an integer (int).
# - is_secure should be a boolean (bool).
# - The function should be annotated to return a dictionary where keys are
#   strings and values are of any type.

def get_service_config(service_name: str, port: int, is_secure: bool) -> dict[str, Any]:
    """
    Creates a configuration dictionary for a service.
    """
    config = {
        "service": service_name,
        "network": {
            "port": port,
            "is_tls": is_secure
        }
    }
    return config