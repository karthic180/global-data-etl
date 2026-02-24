# Global Data ETL

A Python-based system to fetch country data, store it in a SQLite database, and provide database operations, testing, system info, health checks, and web dashboard access via Streamlit or Flask.

---

## Features

### ETL Pipeline
- Fetch country data (name, region, subregion) from free APIs.
- Store data in SQLite database (`global_data.db`).
- Track fetch metadata: timestamp, API used, fetch method.
- Supports single country or all countries.

### Database Operations
- View database contents.
- Export database in **CSV**, **JSON**, and **Excel** formats.
- Clean database (delete database file).

### Tests
- Run **unit tests** for ETL modules.
- Generate **coverage reports**.
- Run **full ETL pipeline test**.
- Test **Streamlit** and **Flask** UI launches.

### Web Access
- Launch **Streamlit dashboard** for interactive UI.
- Launch **Flask website** for basic web interface.

### System Info
- Display OS, Python version, CPU cores, and memory.

### Health Check
- Verify database file existence.
- Check if **Streamlit** and **Flask** are installed.

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