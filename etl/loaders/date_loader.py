import pandas as pd

from etl.config import PROCESSED_DATA_DIR
from etl.utils.logger import get_logger

logger = get_logger(__name__)


def load_dates(connection):
    """
    Load unique dates into dim_date.
    """
    file_path = PROCESSED_DATA_DIR / "jobs_clean.csv"

    logger.info(f"Reading processed data from {file_path}")

    df = pd.read_csv(file_path)

    # Convert to datetime
    df["created"] = pd.to_datetime(df["created"])

    # Keep only the date part
    df["full_date"] = df["created"].dt.date

    dates = (
        df["full_date"]
        .drop_duplicates()
        .sort_values()
    )

    cursor = connection.cursor()

    query = """
    INSERT IGNORE INTO dim_date
    (full_date, year, month, month_name, day, weekday_name)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    inserted_count = 0

    for date in dates:

        timestamp = pd.Timestamp(date)

        cursor.execute(
            query,
            (
                date,
                timestamp.year,
                timestamp.month,
                timestamp.strftime("%B"),
                timestamp.day,
                timestamp.strftime("%A"),
            ),
        )

        if cursor.rowcount == 1:
            inserted_count += 1

    connection.commit()

    logger.info(f"Inserted {inserted_count} new dates.")