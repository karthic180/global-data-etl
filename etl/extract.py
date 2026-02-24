import requests

MAIN_API = "https://restcountries.com/v3.1/all"
FALLBACK_API = "https://restcountries.com/v3.1/name/"

def fetch_countries():
    try:
        response = requests.get(MAIN_API, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Main API failed: {e}")
        return []

def fetch_country(country_name):
    try:
        response = requests.get(f"{FALLBACK_API}{country_name}", timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data
        return [data]
    except Exception as e:
        print(f"Fallback API failed: {e}")
        return []