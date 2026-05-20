import subprocess
import sys
import platform

def check_host_status(hostname: str) -> str:
    """
    Checks if a host is online by pinging it a limited number of times.

    Args:
        hostname (str): The hostname or IP address to ping.

    Returns:
        'online' if the host is reachable (ping exit code 0), 'offline' otherwise.
    
    Raises:
        TypeError: If hostname is not a string.
        ValueError: If hostname is not a non-empty string.
    """
    # Input validation
    if not isinstance(hostname, str):
        raise TypeError(f"Hostname must be a string, recieved {type(hostname).__name__!r}")
    if not hostname.strip():
        raise ValueError("Hostname must be non-empty")
    
    # Construct and run the ping command. Make sure that subprocess does not raise an exception on non-zero exit codes.
    if platform.system() == "Windows":
        cmd = ["ping", hostname, "-w", "5000"] # translates to: ping hostname -w 5
    else:
        cmd = ["ping", hostname, "-W", "5"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return "online"
        else:
            return "offline"
    # Handle relevant exceptions.
    except FileNotFoundError as err:
        print(f"The command '{cmd[0]}' was not found on this system.")
    except subprocess.TimeoutExpired as err:
        print(f"Command timed out after {err.timeout} seconds")
        return "offline"
    except Exception as err:
        print(err)

# A typically reachable host
status1 = check_host_status("8.8.8.8") 
print(f"Status of 8.8.8.8: {status1}")  # Expected: 'online'
 
# A private, likely unreachable IP address
status2 = check_host_status("10.255.255.1")
print(f"Status of 10.255.255.1: {status2}") # Expected: 'offline'