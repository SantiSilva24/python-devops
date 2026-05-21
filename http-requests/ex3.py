import requests
from typing import List, Dict, Optional, Any

def get_incident_summary(api_url: str, api_key: str, service_id: str) -> Optional[List[str]]:
    """
    Fetches open incidents for a specific service and formats them into a list
    of summary strings.

    Args:
        api_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        service_id (str): The ID of the service to query.

    Returns:
        A list of formatted incident summary strings on success, or None on an HTTP error.
    
    Raises:
        ValueError: If any argument is an empty or invalid string.
    """
    # Add validation to ensure all arguments are non-empty strings.
    for parameter in [api_url, api_key, service_id]:
        if not isinstance(parameter, str):
            raise TypeError(f"{parameter} must be a string, recieved {type(parameter).__name__!r}")
        if not parameter.strip():
            raise ValueError(f"{parameter} must be non-empty")
    
    # Prepare the request components (URL, headers, params).
    incidents_url = f"{api_url}/incidents"
    query_headers = {
        "Authorization": f"Bearer {api_key}"
    }
    query_params = {
        "service_ids[]": service_id,
        "statuses[]": "triggered",
    }

    # Make the GET request using the requests library, and build the list of parsed incidents.
    try:
        response = requests.get(incidents_url, headers=query_headers, params=query_params, timeout=10)
        response.raise_for_status()                      # raises HTTPError on 4xx/5xx

        incidents = response.json()
        formatted_incidents = []

        # .get() safely returns [] if "incidents" key is missing
        for incident in incidents.get("incidents", []):
            summary = f"[{incident['urgency'].upper()}] {incident['id']}: {incident['title']}"
            formatted_incidents.append(summary)

        return formatted_incidents

    except requests.exceptions.HTTPError:
        return None
    except requests.exceptions.ConnectionError:
        return None

    