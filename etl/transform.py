def transform_country_data(country):
    # extract common fields safely
    name = country.get("name", {}).get("common") if isinstance(country.get("name"), dict) else country.get("name")
    capital = country.get("capital")[0] if country.get("capital") else None
    lat = country.get("latlng")[0] if country.get("latlng") else None
    lon = country.get("latlng")[1] if country.get("latlng") else None

    return {
        "name": name,
        "region": country.get("region"),
        "population": country.get("population"),
        "area": country.get("area"),
        "capital": capital,
        "lat": lat,
        "lon": lon,
        "temperature": None,   # to be filled if weather API used
        "windspeed": None,
        "timestamp": None
    }

def c_to_f(c):
    if c is None:
        return None
    return round((c * 9/5) + 32, 2)