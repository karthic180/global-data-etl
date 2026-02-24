from etl.extract import fetch_countries
from etl.transform import transform_country_data
from etl.load import insert_country, insert_weather, init_db
from etl.report import pretty_print, save_summary

def run_real_pipeline():
    """Run the full ETL pipeline."""
    init_db()

    # Ask user which country
    selected_country = input("Enter a country name (or 'all' for all countries): ").strip()
    if selected_country.lower() == "all":
        selected_country = None

    countries = fetch_countries(selected_country)
    for c in countries:
        transform_country_data(c)  # Fill temperature, wind, timestamp etc.
        insert_country(c)
        insert_weather(c)

    pretty_print(countries)
    save_summary(countries)