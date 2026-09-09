import pandas as pd

from etl.config import PROCESSED_DATA_DIR
from etl.utils.logger import get_logger

logger = get_logger(__name__)


def validate_data():
    """
    Validate the processed jobs dataset.
    """

    file_path = PROCESSED_DATA_DIR / "jobs_clean.csv"

    logger.info(f"Reading processed data from {file_path}")

    df = pd.read_csv(file_path)

    logger.info(f"Total records: {len(df)}")

    # Missing values
    missing_values = df.isnull().sum()

    logger.info("Missing values by column:")
    logger.info(f"\n{missing_values}")

    # Duplicate job IDs
    duplicate_jobs = df["job_id"].duplicated().sum()

    logger.info(f"Duplicate job IDs: {duplicate_jobs}")

    # Invalid salary ranges
    invalid_salary_ranges = (
        (df["salary_min"] > df["salary_max"])
        .fillna(False)
        .sum()
    )

    logger.info(
        f"Invalid salary ranges: {invalid_salary_ranges}"
    )

    # Negative salaries
    negative_salary_min = (
        (df["salary_min"] < 0)
        .fillna(False)
        .sum()
    )

    negative_salary_max = (
        (df["salary_max"] < 0)
        .fillna(False)
        .sum()
    )

    logger.info(
        f"Negative salary_min values: {negative_salary_min}"
    )

    logger.info(
        f"Negative salary_max values: {negative_salary_max}"
    )

    # Date validation
    dates = pd.to_datetime(
        df["created"],
        errors="coerce",
        utc=True
    )

    invalid_dates = dates.isna().sum()

    logger.info(f"Invalid dates: {invalid_dates}")

    future_dates = (
        dates > pd.Timestamp.now(tz="UTC")
    ).sum()

    logger.info(f"Future dates: {future_dates}")

    logger.info("Data validation completed.")


if __name__ == "__main__":
    validate_data()