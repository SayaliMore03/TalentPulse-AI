import mysql.connector

from etl.config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE,
    MYSQL_USER,
    MYSQL_PASSWORD,
)

from etl.loaders.company_loader import load_companies
from etl.loaders.location_loader import load_locations
from etl.loaders.category_loader import load_categories
from etl.loaders.date_loader import load_dates
from etl.loaders.fact_loader import load_fact_jobs

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


def load_to_database():
    """
    Load cleaned data into the MySQL warehouse.
    """

    connection = connect_database()

    try:
        load_companies(connection)
        load_locations(connection)
        load_categories(connection)
        load_dates(connection)
        load_fact_jobs(connection)

    finally:
        connection.close()

        logger.info(
            "Database connection closed."
        )


def main():
    """
    Run the database loading stage independently.
    """

    load_to_database()


if __name__ == "__main__":
    main()