import pandas as pd
import mysql.connector

from etl.config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE,
    MYSQL_USER,
    MYSQL_PASSWORD,
    PROCESSED_DATA_DIR,
)
from etl.utils.logger import get_logger

logger = get_logger(__name__)


def connect_database():
    """
    Create and return a MySQL database connection.
    """
    logger.info("Connecting to MySQL database...")

    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
    )

    logger.info("Connected to MySQL successfully.")

    return connection


def load_companies(connection):
    """
    Load unique companies into dim_company.
    """
    file_path = PROCESSED_DATA_DIR / "jobs_clean.csv"

    logger.info(f"Reading processed data from {file_path}")

    df = pd.read_csv(file_path)

    companies = (
        df["company"]
        .dropna()
        .drop_duplicates()
        .sort_values()
    )

    cursor = connection.cursor()

    insert_query = """
    INSERT IGNORE INTO dim_company (company_name)
    VALUES (%s)
    """

    for company in companies:
        cursor.execute(insert_query, (company,))

    connection.commit()

    logger.info(f"Inserted {len(companies)} companies.")


def main():

    connection = connect_database()

    load_companies(connection)

    connection.close()

    logger.info("Database connection closed.")


if __name__ == "__main__":
    main()