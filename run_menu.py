import os
import sys
import sqlite3
import subprocess
import time
from datetime import datetime
import requests
import pandas as pd
from tabulate import tabulate

# -----------------------------
# Database Configuration
# -----------------------------
DB_PATH = "global_data.db"

def init_db():
    """Initialize SQLite database and table if missing"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            name TEXT,
            region TEXT,
            state_province TEXT,
            temperature REAL,
            windspeed REAL,
            timestamp TEXT,
            fetch_method TEXT,
            api_used TEXT
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------
# ETL Functions
# -----------------------------
def fetch_country_data(name):
    """Fetch country data from free API with fallback"""
    countries = []
    try:
        if name.lower() == "all":
            response = requests.get("https://restcountries.com/v3.1/all")
            response.raise_for_status()
            data = response.json()
            method = "all"
            api_used = "restcountries.com v3.1"
        else:
            response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
            response.raise_for_status()
            data = response.json()
            method = "single"
            api_used = "restcountries.com v3.1"
    except Exception as e:
        print(f"Failed to fetch country data: {e}")
        return []

    for c in data:
        country = {
            "name": c.get("name", {}).get("common", ""),
            "region": c.get("region", ""),
            "state_province": c.get("subregion", ""),
            "temperature": None,
            "windspeed": None,
            "timestamp": datetime.now().isoformat(),
            "fetch_method": method,
            "api_used": api_used
        }
        countries.append(country)
    return countries

def insert_country(conn, country):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO countries
        (name, region, state_province, temperature, windspeed, timestamp, fetch_method, api_used)
        VALUES (:name, :region, :state_province, :temperature, :windspeed, :timestamp, :fetch_method, :api_used)
    """, country)
    conn.commit()

def run_etl():
    print("\nRunning ETL pipeline...")
    init_db()
    conn = sqlite3.connect(DB_PATH)
    country_name = input("Enter a country name (or 'all' for all countries): ").strip()
    countries = fetch_country_data(country_name)
    for country in countries:
        insert_country(conn, country)
        print("\n--- Country Data ---")
        print(tabulate([list(country.values())], headers=list(country.keys()), tablefmt="fancy_grid"))
    print(f"\nTotal countries processed: {len(countries)}")
    conn.close()
    input("\nPress Enter to return to menu...")

# -----------------------------
# Database Operations
# -----------------------------
def view_db():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM countries")
    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    print("\n--- Database Contents ---")
    if rows:
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
    else:
        print("Database is empty.")
    conn.close()
    input("\nPress Enter to return to menu...")

def export_db():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM countries", conn)
    conn.close()

    while True:
        print("\n--- Export Menu ---")
        print("1. CSV")
        print("2. JSON")
        print("3. Excel")
        print("4. Back to Database Menu")
        choice = input("Choose export format [1-4]: ").strip()
        if choice == "1":
            df.to_csv("countries_export.csv", index=False)
            print("Data exported to countries_export.csv")
        elif choice == "2":
            df.to_json("countries_export.json", orient="records", indent=4)
            print("Data exported to countries_export.json")
        elif choice == "3":
            try:
                df.to_excel("countries_export.xlsx", index=False)
                print("Data exported to countries_export.xlsx")
            except Exception as e:
                print(f"Failed to export Excel: {e}")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

def clean_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Database {DB_PATH} removed.")
    else:
        print("No database found to remove.")
    input("\nPress Enter to return to menu...")

def database_menu():
    while True:
        print("\n--- Database Menu ---")
        print("1. View database contents")
        print("2. Export database")
        print("3. Clean database")
        print("4. Back to Main Menu")
        choice = input("Enter your choice [1-4]: ").strip()
        if choice == "1":
            view_db()
        elif choice == "2":
            export_db()
        elif choice == "3":
            clean_db()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Select 1-4.")

# -----------------------------
# Tests
# -----------------------------
def run_tests():
    subprocess.run([sys.executable, "-m", "pytest", "tests"], check=False)
    input("\nPress Enter to return to menu...")

def coverage_report():
    subprocess.run([sys.executable, "-m", "pytest", "--cov=.", "tests"], check=False)
    input("\nPress Enter to return to menu...")

def full_etl_test():
    subprocess.run([sys.executable, "-m", "pytest", "tests/test_full_pipeline.py"], check=False)
    input("\nPress Enter to return to menu...")

def tests_menu():
    while True:
        print("\n=== Tests Menu ===")
        print("1. Run tests")
        print("2. Run coverage report")
        print("3. Run full ETL pipeline test")
        print("4. Back to Main Menu")
        choice = input("Enter your choice [1-4]: ").strip()
        if choice == "1":
            run_tests()
        elif choice == "2":
            coverage_report()
        elif choice == "3":
            full_etl_test()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Select 1-4.")

# -----------------------------
# Web UI Submenu
# -----------------------------
def launch_streamlit():
    try:
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "web_ui_streamlit.py"])
        print("Streamlit launched.")
    except Exception as e:
        print(f"Failed to launch Streamlit: {e}")

def launch_flask():
    try:
        subprocess.Popen([sys.executable, "web_ui_flask.py"])
        print("Flask launched.")
    except Exception as e:
        print(f"Failed to launch Flask: {e}")

def web_access_menu():
    while True:
        print("\n=== Web Access ===")
        print("1. Streamlit Dashboard")
        print("2. Flask Website")
        print("3. Back to Main Menu")
        choice = input("Enter your choice [1-3]: ").strip()
        if choice == "1":
            launch_streamlit()
        elif choice == "2":
            launch_flask()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Select 1-3.")

# -----------------------------
# System Info & Health
# -----------------------------
def system_info():
    print("\nSystem Info (placeholder)")
    input("\nPress Enter to return to menu...")

def health_check():
    print("\nHealth Check (placeholder)")
    input("\nPress Enter to return to menu...")

# -----------------------------
# Main Menu
# -----------------------------
def main_menu():
    while True:
        print("\n==== Main Menu ====")
        print("1. Run ETL pipeline")
        print("2. Database operations")
        print("3. Tests")
        print("4. System information")
        print("5. Health check")
        print("6. Exit")
        print("7. Web Access")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            run_etl()
        elif choice == "2":
            database_menu()
        elif choice == "3":
            tests_menu()
        elif choice == "4":
            system_info()
        elif choice == "5":
            health_check()
        elif choice == "6":
            print("Exiting... Goodbye!")
            sys.exit(0)
        elif choice == "7":
            web_access_menu()
        else:
            print("Invalid choice. Select 1-7.")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main_menu()