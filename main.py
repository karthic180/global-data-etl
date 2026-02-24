import logging
from etl.load import init_db
from etl.pipeline import run
from etl.report import export_summary_to_csv
from etl.logger_config import setup_logger


if __name__ == "__main__":

    logger = setup_logger()

    logger.info("Starting Global Data ETL Pipeline")

    init_db()
    run(limit=10)

    logger.info("ETL processing complete")

    file_path = export_summary_to_csv()
    logger.info(f"Summary exported to {file_path}")

    logger.info("Pipeline finished successfully")