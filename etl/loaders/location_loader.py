import pandas as pd

from etl.config import PROCESSED_DATA_DIR
from etl.utils.logger import get_logger

logger = get_logger(__name__)


def load_locations(connection):
    """
    Load unique locations into dim_location.
    """
    file_path = PROCESSED_DATA_DIR / "jobs_clean.csv"

    logger.info(f"Reading processed data from {file_path}")

    df = pd.read_csv(file_path)

    locations = (
        df["location"]
        .dropna()
        .drop_duplicates()
        .sort_values()
    )

    cursor = connection.cursor()

    query = """
    INSERT IGNORE INTO dim_location (location_name)
    VALUES (%s)
    """

    inserted_count = 0

    for location in locations:
        cursor.execute(query, (location,))

        if cursor.rowcount == 1:
            inserted_count += 1

    connection.commit()

    logger.info(f"Inserted {inserted_count} new locations.")