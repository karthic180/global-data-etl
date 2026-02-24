import sqlite3
import threading
import webbrowser
from flask import Flask, render_template, request, jsonify
from etl.load import init_db, fetch_country_data, insert_country, DB_PATH
import pandas as pd
import socket


app = Flask(__name__)


# ---------------------------------------------------
# Utility: find a free port
# ---------------------------------------------------
def find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


# ---------------------------------------------------
# Load database into DataFrame
# ---------------------------------------------------
def load_db():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM countries", conn)
    conn.close()
    return df


# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
@app.route("/")
def home():
    df = load_db()
    count = len(df)
    return render_template("home.html", count=count)


# ---------------------------------------------------
# RUN ETL
# ---------------------------------------------------
@app.route("/etl", methods=["GET", "POST"])
def etl():
    message = None
    results = []

    if request.method == "POST":
        query = request.form.get("country", "").strip()

        if query:
            init_db()
            conn = sqlite3.connect(DB_PATH)
            countries = fetch_country_data(query)

            for country in countries:
                status = insert_country(conn, country)
                results.append({"name": country["name"], "status": status})

            conn.close()
            message = f"Processed {len(results)} countries."

    return render_template("etl.html", message=message, results=results)


# ---------------------------------------------------
# VIEW DATABASE
# ---------------------------------------------------
@app.route("/database")
def database():
    df = load_db()
    rows = df.to_dict(orient="records")
    headers = df.columns.tolist()
    return render_template("database.html", rows=rows, headers=headers)


# ---------------------------------------------------
# CHARTS (Temperature Trends)
# ---------------------------------------------------
@app.route("/charts")
def charts():
    df = load_db()

    if df.empty:
        return render_template("charts.html", countries=[], data_available=False)

    countries = sorted(df["name"].unique())
    return render_template("charts.html", countries=countries, data_available=True)


# AJAX endpoint to fetch chart data
@app.route("/chart-data")
def chart_data():
    country = request.args.get("country")

    df = load_db()
    df = df[df["name"] == country]

    if df.empty:
        return jsonify({"ok": False})

    row = df.iloc[0]

    # Create two points so Chart.js can draw a line
    timestamps = [row["timestamp"], row["timestamp"]]
    temp_c = [row["temperature_c"], row["temperature_c"]]
    temp_f = [row["temperature_f"], row["temperature_f"]]

    return jsonify({
        "ok": True,
        "timestamps": timestamps,
        "temp_c": temp_c,
        "temp_f": temp_f
    })


# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------
@app.route("/health")
def health():
    import os
    import shutil
    import requests

    results = {}

    try:
        r = requests.get("https://restcountries.com/v3.1/all", timeout=5)
        results["API Availability"] = "PASS" if r.status_code == 200 else "FAIL"
    except Exception:
        results["API Availability"] = "FAIL"

    if os.path.exists(DB_PATH):
        size_mb = round(os.path.getsize(DB_PATH) / (1024 * 1024), 3)
        results["Database Size"] = f"{size_mb} MB"
    else:
        results["Database Size"] = "No database found"

    total, used, free = shutil.disk_usage(os.getcwd())
    results["Disk Total"] = f"{round(total / (1024**3), 2)} GB"
    results["Disk Used"] = f"{round(used / (1024**3), 2)} GB"
    results["Disk Free"] = f"{round(free / (1024**3), 2)} GB"

    return jsonify(results)


# ---------------------------------------------------
# Run Flask with auto-selected port
# ---------------------------------------------------
def run_flask():
    port = find_free_port()
    url = f"http://localhost:{port}"

    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(port=port, debug=False)


if __name__ == "__main__":
    run_flask()
