import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime

from etl.load import init_db, fetch_country_data, insert_country, DB_PATH


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Global Data ETL Dashboard",
    layout="wide"
)


# ---------------------------------------------------
# DATABASE LOADER
# ---------------------------------------------------
def load_db():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM countries", conn)
    conn.close()
    return df


# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Home", "Run ETL", "View Database", "Charts", "Health Check", "System Info"]
)


# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
if page == "Home":
    st.title("Global Data ETL Dashboard")
    st.write("A simple dashboard for viewing and updating global country data.")

    df = load_db()

    st.subheader("Quick Stats")
    st.metric("Countries in database", len(df))

    if not df.empty:
        st.subheader("Latest Entries")
        st.dataframe(df.tail(10), use_container_width=True)


# ---------------------------------------------------
# RUN ETL
# ---------------------------------------------------
elif page == "Run ETL":
    st.title("Run ETL Pipeline")

    query = st.text_input("Enter a country name (or 'all'):", value="gb")

    if st.button("Run ETL"):
        if not query.strip():
            st.error("Please enter a valid country name.")
        else:
            init_db()
            conn = sqlite3.connect(DB_PATH)
            countries = fetch_country_data(query)

            results = []
            for country in countries:
                status = insert_country(conn, country)
                results.append({
                    "name": country["name"],
                    "status": status
                })

            conn.close()

            st.success(f"Processed {len(results)} countries.")
            st.dataframe(pd.DataFrame(results), use_container_width=True)


# ---------------------------------------------------
# VIEW DATABASE
# ---------------------------------------------------
elif page == "View Database":
    st.title("Database Contents")

    df = load_db()

    if df.empty:
        st.warning("Database is empty.")
    else:
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            "countries.csv",
            "text/csv"
        )


# ---------------------------------------------------
# CHARTS (Temperature Trends)
# ---------------------------------------------------
elif page == "Charts":
    st.title("Temperature Trends")

    df = load_db()

    if df.empty:
        st.warning("Database is empty.")
    else:
        countries = sorted(df["name"].unique())
        selected = st.selectbox("Choose a country:", countries)

        country_df = df[df["name"] == selected].sort_values("timestamp")

        if country_df.empty:
            st.warning("No data available for this country.")
        else:
            st.subheader(f"Temperature Trend for {selected}")

            chart_df = country_df[["timestamp", "temperature_c", "temperature_f"]]
            chart_df["timestamp"] = pd.to_datetime(chart_df["timestamp"])
            chart_df = chart_df.set_index("timestamp")

            st.line_chart(chart_df)


# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------
elif page == "Health Check":
    import os
    import shutil
    import requests

    st.title("Health Check")

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

    st.json(results)


# ---------------------------------------------------
# SYSTEM INFO
# ---------------------------------------------------
elif page == "System Info":
    import platform

    st.title("System Information")

    st.write({
        "Python Version": platform.python_version(),
        "Operating System": f"{platform.system()} {platform.release()}",
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Timestamp (UTC)": datetime.utcnow().isoformat()
    })
