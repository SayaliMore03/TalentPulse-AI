import pandas as pd

from etl.config import PROCESSED_DATA_DIR
from etl.utils.logger import get_logger

logger = get_logger(__name__)


def load_categories(connection):
    """
    Load unique job categories into dim_category.
    """
    file_path = PROCESSED_DATA_DIR / "jobs_clean.csv"

    logger.info(f"Reading processed data from {file_path}")

    df = pd.read_csv(file_path)

    categories = (
        df["category"]
        .dropna()
        .drop_duplicates()
        .sort_values()
    )

    cursor = connection.cursor()

    query = """
    INSERT IGNORE INTO dim_category (category_name)
    VALUES (%s)
    """

    inserted_count = 0

    for category in categories:
        cursor.execute(query, (category,))

        if cursor.rowcount == 1:
            inserted_count += 1

    connection.commit()

    logger.info(f"Inserted {inserted_count} new categories.")