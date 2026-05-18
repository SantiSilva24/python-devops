from functools import wraps

def sanitize_hostname(func):
    """
    A decorator that finds a 'hostname' keyword argument, sanitizes it
    (lowercase, stripped whitespace), and passes it to the wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        hostname = kwargs.get("hostname")
        if not hostname:
            return None
        santized_hostname = hostname.strip().lower()
        print(f"Santitized {hostname} to {santized_hostname}")
        kwargs["hostname"] = santized_hostname
        value = func(*args, **kwargs)
        return value
    return wrapper
    
@sanitize_hostname
def connect_to_host(*, hostname):
    """Establishes a connection to a host."""
    print(f"Connecting to sanitized hostname: '{hostname}'")
    return f"Connected to {hostname}"
 
# The decorator will sanitize '  PROD-API.local  ' to 'prod-api.local'
connect_to_host(hostname="  PROD-API.local  ")