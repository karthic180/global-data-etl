import sqlite3
import os
from etl.load import fetch_country_data, insert_country
from datetime import datetime

DB_PATH = "test_global_data.db"

def setup_module(module):
    # Create test database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            name TEXT, region TEXT, state_province TEXT,
            temperature REAL, windspeed REAL, timestamp TEXT,
            fetch_method TEXT, api_used TEXT
        )
    """)
    conn.commit()
    conn.close()

def teardown_module(module):
    # Clean up test database
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_fetch_country_data():
    result = fetch_country_data("gb")
    assert len(result) > 0
    assert result[0]["name"].lower() in ["united kingdom", "gb"]

def test_insert_country():
    conn = sqlite3.connect(DB_PATH)
    country = {
        "name": "Testland",
        "region": "TestRegion",
        "state_province": "TestProvince",
        "temperature": 25,
        "windspeed": 5,
        "timestamp": datetime.utcnow().isoformat(),
        "fetch_method": "latest",
        "api_used": "mock"
    }
    insert_country(conn, country)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM countries WHERE name='Testland'")
    rows = cursor.fetchall()
    assert len(rows) == 1
    conn.close()