import requests

def trigger_jenkins_job(jenkins_url: str, job_name: str, auth_token: str) -> bool:
    """
    Triggers a Jenkins job by making an authenticated POST request.

    Args:
        jenkins_url (str): The base URL of the Jenkins server.
        job_name (str): The name of the job to trigger.
        auth_token (str): The authentication token.

    Returns:
        bool: True if the job was triggered successfully (status 201), False otherwise.
    
    Raises:
        ValueError: If any argument is an empty or invalid string.
    """
    # Add validation to ensure all arguments are non-empty strings. Raise a ValueError if any argument is invalid.
    for parameter in [jenkins_url, job_name, auth_token]:
        if not isinstance(parameter, str):
            raise TypeError(f"{parameter} must be a string, recieved {type(parameter).__name__!r}")
        if not parameter.strip():
            raise ValueError(f"{parameter} must be non-empty")
    
    # Send a post request using the requests library to the URL provided in the description. Make sure to include the necessary headers.
    trigger_url = f"{jenkins_url}/job/{job_name}/build"
    query_headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    try:
        response = requests.post(trigger_url, headers=query_headers, timeout=10)
        return response.status_code == 201
    except requests.exceptions.ConnectionError:
        # Simulates/handles network failure — no route to host, DNS failure, etc.
        return False
    
    