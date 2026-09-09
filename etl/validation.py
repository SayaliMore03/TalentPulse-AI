import pandas as pd

from etl.utils.logger import get_logger

logger = get_logger(__name__)


def validate_data(file_path):
    """
    Validate the processed jobs dataset.
    """

    logger.info(
        f"Reading processed data from {file_path}"
    )

    df = pd.read_csv(file_path)

    logger.info(
        f"Total records: {len(df)}"
    )

    # --------------------------------------------------
    # Missing values
    # --------------------------------------------------

    missing_values = df.isnull().sum()

    logger.info(
        f"Missing values by column:\n{missing_values}"
    )

    # --------------------------------------------------
    # Duplicate job IDs
    # --------------------------------------------------

    duplicate_jobs = df["job_id"].duplicated().sum()

    logger.info(
        f"Duplicate job IDs: {duplicate_jobs}"
    )

    # --------------------------------------------------
    # Invalid salary ranges
    # --------------------------------------------------

    invalid_salary_ranges = (
        (df["salary_min"] > df["salary_max"])
        .fillna(False)
        .sum()
    )

    logger.info(
        f"Invalid salary ranges: "
        f"{invalid_salary_ranges}"
    )

    # --------------------------------------------------
    # Negative salaries
    # --------------------------------------------------

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
        f"Negative salary_min values: "
        f"{negative_salary_min}"
    )

    logger.info(
        f"Negative salary_max values: "
        f"{negative_salary_max}"
    )

    # --------------------------------------------------
    # Date validation
    # --------------------------------------------------

    dates = pd.to_datetime(
        df["created"],
        errors="coerce",
        utc=True
    )

    invalid_dates = dates.isna().sum()

    logger.info(
        f"Invalid dates: {invalid_dates}"
    )

    # Compare calendar dates rather than exact timestamps.
    # Jobs created later today are still valid.

    today = pd.Timestamp.now(tz="UTC").date()

    future_dates = (
        dates.dt.date > today
    ).sum()

    logger.info(
        f"Future dates: {future_dates}"
    )

    # --------------------------------------------------
    # Validation completed
    # --------------------------------------------------

    logger.info(
        "Data validation completed."
    )

    return True


if __name__ == "__main__":
    from etl.config import PROCESSED_DATA_DIR

    validate_data(
        PROCESSED_DATA_DIR / "jobs_clean.csv"
    )