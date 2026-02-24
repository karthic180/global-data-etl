import csv

def pretty_print_summary(countries):
    """Pretty-print country info with °C → °F conversion."""
    for c in countries:
        temp_c = c.get("temperature")
        temp_f = (temp_c * 9/5 + 32) if temp_c is not None else None
        c["temperature_F"] = temp_f

        print({
            "name": c.get("name"),
            "region": c.get("region"),
            "population": c.get("population"),
            "area": c.get("area"),
            "capital": c.get("capital"),
            "lat": c.get("lat"),
            "lon": c.get("lon"),
            "temperature": temp_c,
            "temperature_F": temp_f,
            "windspeed": c.get("windspeed"),
            "timestamp": c.get("timestamp")
        })


def save_summary_csv(countries, filepath="data/summary.csv"):
    """Save country data summary to CSV"""
    fieldnames = ["name","region","population","area","capital",
                  "lat","lon","temperature","temperature_F","windspeed","timestamp"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in countries:
            writer.writerow({k: c.get(k) for k in fieldnames})