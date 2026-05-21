import requests
import pycountry
from datetime import date

def is_today_a_public_holiday(country_code: str) -> bool:
    """
    Checks if today is a public holiday for a given country by querying an API.

    Args:
        country_code (str): The two-letter country code (e.g., "US").

    Returns:
        bool: True if today is a public holiday, False otherwise.
    
    Raises:
        TypeError: If country_code is not a string.
    """
    # Input validation
    if not isinstance(country_code, str):
        raise TypeError(f"Hostname must be a string, recieved {type(country_code).__name__!r}")
    if not country_code.strip():
        raise ValueError("Hostname must be non-empty")
    
    # Guard clause to validate that `country_code` is a string with two characters
    if len(country_code) != 2 or not pycountry.countries.get(alpha_2=country_code.upper()):
        raise ValueError(f"'{country_code}' is not a valid ISO 3166-1 alpha-2 country code")
    
    # Get today's date using the `datetime` module.
    today = date.today()

    # Make a GET request using `requests.get()`, passing the URL and params.
    search_url = "https://api.example.com/v1/holidays"
    query_params = {
        "country": country_code,
        "year": today.year
    }
    response = requests.get(search_url, params=query_params, timeout=10)
    response.raise_for_status()

    # parse reponse bode as JSON
    holidays = response.json()

    # Return whether today is a holiday based on the results of the API.
    for holiday in holidays:
        if holiday["date"] == today.isoformat():
            return True
    return False