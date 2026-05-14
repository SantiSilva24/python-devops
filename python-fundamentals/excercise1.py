"""
Validate a given dictionary based on certain rules.
    Rules:
    - Required keys: service_name, env, port
    - env must be one of: dev, staging, prod
    - service_name must be a non-empty string
    - port must be an integer between 1 and 65535
"""

ALLOWED_ENVS = {"dev", "staging", "prod"}
REQUIRED_KEYS = {"service_name", "env", "port"}


def validate_config(config: dict) -> bool:
    # Validate required keys
    missing_keys = REQUIRED_KEYS - config.keys()
    if missing_keys:
        print(f"Missing required keys: {', '.join(missing_keys)}")
        return False

    # Validate environment
    if config["env"] not in ALLOWED_ENVS:
        print(
            f"Unsupported environment '{config['env']}'. "
            f"Allowed values: {', '.join(ALLOWED_ENVS)}"
        )
        return False

    # Validate service name
    service_name = config["service_name"]
    
    # Validate whitespace-only stings with .strip()
    if not isinstance(service_name, str) or not service_name.strip():
        print("service_name must be a non-empty string")
        return False

    # Validate port
    port = config["port"]

    if not isinstance(port, int) or not (1 <= port <= 65535):
        print("port must be an integer between 1 and 65535")
        return False

    return True


config = {
    "service_name": "auth-service",
    "env": "production",
    "port": 8080,
}

print(validate_config(config))