

# Global Data ETL

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/karthic180/global-data-etl/python-tests.yml)](https://github.com/karthic180/global-data-etl/actions)
[![Coverage Status](https://img.shields.io/badge/Coverage-50%25-yellow)](https://github.com/karthic180/global-data-etl)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

It is a comprehensive Python project that demonstrates end-to-end data engineering and analytics workflows. It is designed for learning, experimentation, and showcasing a real-world ETL process.

## Key features

ETL Pipeline: Fetch country-level metadata from public APIs (RestCountries), transform it, and store it in a local SQLite database.

Database Operations: View, export (CSV, JSON, Excel), and manage the database contents.

Testing & Coverage: Includes unit tests and full pipeline tests with code coverage reporting.

Web Access Interfaces: Optional Streamlit dashboard and Flask web interface for interactive data exploration.

System & Health Checks: Built-in utilities to verify environment, database integrity, and service availability.

Extensible & Modular: Designed for easy expansion with additional APIs, data sources, or analytics workflows.

This project is ideal for anyone looking to understand or demonstrate Python-based ETL pipelines, database management, and lightweight web interfaces for data analytics.

---

## Requirements

- Python 3.8+
- Packages:
  - `requests`
  - `pandas`
  - `tabulate`
  - `openpyxl`
  - `pytest`, `pytest-cov`
  - `streamlit`
  - `flask`
  - `psutil`

Install missing packages automatically via menu, or manually:

```bash
pip install requests pandas tabulate openpyxl pytest pytest-cov streamlit flask psutil
Installation

Clone the repository:

git clone https://github.com/karthic180/global-data-etl.git
cd global-data-etl

Run the menu script:

python run_menu.py
Usage

After starting run_menu.py, you will see the main menu:

==== Main Menu ====
1. Run ETL pipeline
2. Database operations
3. Tests
4. System information
5. Health check
6. Exit
7. Web Access
1. ETL Pipeline

Enter a country name (e.g., gb) or all for all countries.

Data will be inserted into the database.

2. Database Operations

View database contents in a formatted table.

Export database to CSV, JSON, and Excel.

Clean the database by removing the SQLite file.

3. Tests

Run unit tests for ETL modules.

Generate coverage reports (~50% coverage by default).

Run a full ETL pipeline test.

Check if Streamlit/Flask UI launches successfully.

4. System Information

Displays OS, Python version, CPU, and RAM.

5. Health Check

Checks if the database exists.

Checks if Streamlit and Flask are installed.

6. Exit

Exit the menu.

7. Web Access

Launch Streamlit dashboard or Flask website for interactive web access.

Project Structure
global-data-etl/
│
├─ etl/
│   ├─ load.py            # Fetch country data, insert into DB
│   └─ transform.py       # Optional transformations
│
├─ tests/
│   ├─ test_load.py
│   ├─ test_transform.py
│   └─ test_full_pipeline.py
│
├─ web_ui_streamlit.py    # Streamlit dashboard
├─ web_ui_flask.py        # Flask website
├─ run_menu.py            # Menu-driven launcher
├─ global_data.db         # SQLite DB (created at runtime)
└─ README.md
Example Usage

Run ETL for UK:

Enter a country name (or 'all' for all countries): gb

Inserted United Kingdom into database
ETL complete. Total countries processed: 1

Export database:

Database exported to CSV, JSON, Excel

Run coverage report:

pytest --cov=. tests
Notes

The project uses SQLite for simplicity and easy portability.

Streamlit and Flask are optional; you can run ETL and database operations entirely from the menu.

The ETL function currently sets temperature and windspeed as None for future integration with weather APIs.

License

This project is licensed under the MIT License.
