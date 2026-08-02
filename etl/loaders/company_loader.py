import pandas as pd

from etl.config import PROCESSED_DATA_DIR
from etl.utils.logger import get_logger

logger = get_logger(__name__)


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

    inserted_count = 0

    for company in companies:
        cursor.execute(insert_query, (company,))

        if cursor.rowcount == 1:
            inserted_count += 1

    connection.commit()

    logger.info(f"Inserted {inserted_count} new companies.")