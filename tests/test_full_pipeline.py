import sqlite3
import os
from run_menu import init_db, run_etl, DB_PATH

def test_full_pipeline(monkeypatch):
    init_db()
    
    # Mock input to fetch 'gb'
    monkeypatch.setattr("builtins.input", lambda _: "gb")
    run_etl()
    
    # Check database contents
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM countries WHERE name LIKE 'United Kingdom%'")
    rows = cursor.fetchall()
    conn.close()
    
    assert len(rows) > 0