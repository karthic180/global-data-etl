import os
import sqlite3
import requests
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", "global_data.db")


# ---------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS countries (
        name TEXT PRIMARY KEY,
        region TEXT,
        state_province TEXT,
        temperature_c REAL,
        temperature_f REAL,
        conditions TEXT,
        timestamp TEXT,
        last_updated TEXT,
        fetch_method TEXT,
        api_used TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------
# WEATHER LOOKUP (NO LAT/LON REQUIRED)
# ---------------------------------------------------

def decode_weathercode(code):
    mapping = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Severe thunderstorm with hail"
    }
    return mapping.get(code, "Unknown")


def fetch_weather(city_name):
    """
    Weather is fetched by city/country name instead of lat/lon.
    Open-Meteo supports geocoding by name.
    """

    # 1. Geocode name → lat/lon
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
        g = requests.get(geo_url, timeout=5).json()

        if "results" in g and len(g["results"]) > 0:
            lat = g["results"][0]["latitude"]
            lon = g["results"][0]["longitude"]
        else:
            return {"temperature_c": None, "temperature_f": None, "conditions": None}
    except Exception:
        return {"temperature_c": None, "temperature_f": None, "conditions": None}

    # 2. Fetch weather
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        r = requests.get(url, timeout=5).json()

        if "current_weather" in r:
            temp_c = r["current_weather"]["temperature"]
            temp_f = round((temp_c * 9/5) + 32, 1)
            cond = decode_weathercode(r["current_weather"]["weathercode"])

            return {
                "temperature_c": temp_c,
                "temperature_f": temp_f,
                "conditions": cond
            }
    except Exception:
        pass

    # 3. Fallback: wttr.in
    try:
        url = f"https://wttr.in/{city_name}?format=j1"
        r = requests.get(url, timeout=5).json()

        current = r["current_condition"][0]
        temp_c = float(current["temp_C"])
        temp_f = round((temp_c * 9/5) + 32, 1)
        cond = current["weatherDesc"][0]["value"]

        return {
            "temperature_c": temp_c,
            "temperature_f": temp_f,
            "conditions": cond
        }
    except Exception:
        return {"temperature_c": None, "temperature_f": None, "conditions": None}


# ---------------------------------------------------
# FETCH COUNTRY DATA
# ---------------------------------------------------
def fetch_country_data(query):
    url = "https://restcountries.com/v3.1/all"
    data = requests.get(url, timeout=10).json()

    results = []

    for item in data:
        if not isinstance(item, dict):
            continue

        name = item.get("name", {}).get("common", "")
        region = item.get("region", "")
        subregion = item.get("subregion", "")

        if query.lower() == "all" or query.lower() in name.lower():
            results.append({
                "name": name,
                "region": region,
                "state_province": subregion,
                "timestamp": datetime.utcnow().isoformat(),
                "fetch_method": "latest",
                "api_used": "restcountries.com v3.1"
            })

    return results


# ---------------------------------------------------
# INSERT OR UPDATE COUNTRY
# ---------------------------------------------------
def insert_country(conn, country):
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM countries WHERE name = ?", (country["name"],))
    exists = cursor.fetchone()

    weather = fetch_weather(country["name"])

    if exists:
        cursor.execute("""
            UPDATE countries
            SET region = ?, state_province = ?, temperature_c = ?, temperature_f = ?,
                conditions = ?, last_updated = ?, fetch_method = ?, api_used = ?
            WHERE name = ?
        """, (
            country["region"],
            country["state_province"],
            weather["temperature_c"],
            weather["temperature_f"],
            weather["conditions"],
            datetime.utcnow().isoformat(),
            country["fetch_method"],
            country["api_used"],
            country["name"]
        ))
        conn.commit()
        return "updated"

    cursor.execute("""
        INSERT INTO countries (
            name, region, state_province, temperature_c, temperature_f,
            conditions, timestamp, last_updated, fetch_method, api_used
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        country["name"],
        country["region"],
        country["state_province"],
        weather["temperature_c"],
        weather["temperature_f"],
        weather["conditions"],
        country["timestamp"],
        datetime.utcnow().isoformat(),
        country["fetch_method"],
        country["api_used"]
    ))
    conn.commit()
    return "inserted"
