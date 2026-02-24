import requests
from difflib import get_close_matches
from etl.load import init_db, insert_country, insert_weather
from etl.report import pretty_print_summary, save_summary_csv

MAIN_API = "https://restcountries.com/v3.1/all"
FALLBACK_API = "https://restcountries.com/v3.1/name/"

WEATHER_API = "https://api.open-meteo.com/v1/forecast"

def fetch_countries(input_name="all"):
    try:
        if input_name.lower() == "all":
            resp = requests.get(MAIN_API)
            resp.raise_for_status()
            return resp.json()
        else:
            resp = requests.get(FALLBACK_API + input_name)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        print(f"Main API failed: {e}")
        # fallback exact/fuzzy search
        resp = requests.get(FALLBACK_API + input_name)
        resp.raise_for_status()
        return resp.json()

def fetch_weather(lat, lon):
    """Fetch live weather from Open-Meteo API"""
    if lat is None or lon is None:
        return None, None, None
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
        resp = requests.get(WEATHER_API, params=params)
        resp.raise_for_status()
        data = resp.json()
        weather = data.get("current_weather", {})
        temperature = weather.get("temperature")  # °C
        windspeed = weather.get("windspeed")      # km/h
        timestamp = weather.get("time")
        return temperature, windspeed, timestamp
    except Exception:
        return None, None, None

def transform_country_data(raw_countries, input_name=None):
    country_names = [c.get("name", {}).get("common","") for c in raw_countries]
    transformed = []
    for c in raw_countries:
        name = c.get("name", {}).get("common")
        # fuzzy match
        if input_name and input_name.lower() != "all":
            match = get_close_matches(input_name, [name], cutoff=0.5)
            if not match:
                continue
            name = match[0]

        lat, lon = (c.get("latlng",[None,None])[:2])
        temperature, windspeed, timestamp = fetch_weather(lat, lon)

        country_data = {
            "name": name,
            "region": c.get("region"),
            "population": c.get("population"),
            "area": c.get("area"),
            "capital": c.get("capital",[None])[0] if c.get("capital") else None,
            "lat": lat,
            "lon": lon,
            "temperature": temperature,
            "windspeed": windspeed,
            "timestamp": timestamp
        }
        transformed.append(country_data)
    return transformed

def run_pipeline():
    conn = init_db()
    input_name = input("Enter a country name (or 'all' for all countries): ")
    raw = fetch_countries(input_name)
    transformed = transform_country_data(raw, input_name=input_name)

    for country in transformed:
        insert_country(conn, country)
        insert_weather(conn, country)

    pretty_print_summary(transformed)
    save_summary_csv(transformed)
    print(f"\nTotal countries processed: {len(transformed)}")