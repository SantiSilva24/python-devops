# Define the MaxRetriesExceededError custom exception, accepting `attempts` and `last_exception` as arguments. It should also create a helpful error message to pass to the parent class.

from functools import wraps
import random
import time

class MaxRetriesExceededError(Exception):
    def __init__(self, attempts, last_exception):
        self.attempts = attempts
        self.last_exception = last_exception
        message = f"Max attempts reached: {attempts} in exception: {last_exception}"
        super().__init__(message)
        
def retry_with_backoff(max_attempts, base_delay=1.0, jitter=0.1):
    """
    A decorator factory for retrying a function with validation, exponential
    backoff, jitter, and custom exceptions.
    """
    if not isinstance(max_attempts, int) or max_attempts <= 0:
        raise ValueError("max_attempts must be a positive integer")
    if base_delay < 0:
        raise ValueError("base_delay must be a non-negative number")
    if jitter < 0:
        raise ValueError("jitter must be a non-negative number")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):       
            last_exception = None

            for failure_count in range(1, max_attempts + 1):  # 1-based for readable delay math
                try:
                    return func(*args, **kwargs) # belongs to wrapper 
                                                  
                except Exception as error:        
                    last_exception = error        

                    if failure_count < max_attempts:      
                        delay = base_delay * (2 ** (failure_count - 1))
                        delay += random.uniform(0, jitter)  
                        time.sleep(delay)                  

            # All attempts exhausted — now raise, chaining the original exception
            raise MaxRetriesExceededError(max_attempts, last_exception) from last_exception

        return wrapper     # belongs to decorator
    return decorator       # belongs to retry_with_backoff

# --- Manual test ---
@retry_with_backoff(max_attempts=3, base_delay=0.1, jitter=0.05)
def connect_to_api():
    raise ConnectionError("API is down")

try:
    connect_to_api()
except MaxRetriesExceededError as e:
    print(f"Failed after {e.attempts} attempts. Last error was: {e.last_exception}")
        