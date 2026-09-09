import pandas as pd

from etl.utils.logger import get_logger

logger = get_logger(__name__)


def clean_data(file_path):
    """
    Clean the transformed jobs dataset and save the cleaned data.
    """

    logger.info(
        f"Reading transformed data from {file_path}"
    )

    df = pd.read_csv(file_path)

    initial_rows = len(df)

    # --------------------------------------------------
    # 1. Standardize column names
    # --------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # --------------------------------------------------
    # 2. Standardize text fields
    # --------------------------------------------------

    text_columns = [
        "title",
        "company",
        "location",
        "category",
        "contract_type",
        "contract_time",
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # --------------------------------------------------
    # 3. Convert empty strings to missing values
    # --------------------------------------------------

    df = df.replace(
        r"^\s*$",
        pd.NA,
        regex=True
    )

    # --------------------------------------------------
    # 4. Convert salary columns to numeric
    # --------------------------------------------------

    df["salary_min"] = pd.to_numeric(
        df["salary_min"],
        errors="coerce"
    )

    df["salary_max"] = pd.to_numeric(
        df["salary_max"],
        errors="coerce"
    )

    # --------------------------------------------------
    # 5. Convert created column to datetime
    # --------------------------------------------------

    df["created"] = pd.to_datetime(
        df["created"],
        errors="coerce",
        utc=True
    )

    # --------------------------------------------------
    # 6. Remove duplicate job IDs
    # --------------------------------------------------

    before_duplicates = len(df)

    df = df.drop_duplicates(
        subset="job_id",
        keep="first"
    )

    duplicates_removed = (
        before_duplicates - len(df)
    )

    # --------------------------------------------------
    # 7. Handle invalid salary values
    # --------------------------------------------------

    invalid_min = df["salary_min"] <= 0
    invalid_max = df["salary_max"] <= 0

    invalid_salary_count = (
        invalid_min.fillna(False)
        | invalid_max.fillna(False)
    ).sum()

    df.loc[
        invalid_min.fillna(False),
        "salary_min"
    ] = pd.NA

    df.loc[
        invalid_max.fillna(False),
        "salary_max"
    ] = pd.NA

    # --------------------------------------------------
    # 8. Handle invalid salary ranges
    # --------------------------------------------------

    invalid_range = (
        (df["salary_min"] > df["salary_max"])
        .fillna(False)
    )

    invalid_range_count = invalid_range.sum()

    df.loc[
        invalid_range,
        ["salary_min", "salary_max"]
    ] = pd.NA

    # --------------------------------------------------
    # 9. Save cleaned data
    # --------------------------------------------------

    df.to_csv(
        file_path,
        index=False
    )

    logger.info(
        f"Initial records: {initial_rows}"
    )

    logger.info(
        f"Duplicates removed: {duplicates_removed}"
    )

    logger.info(
        f"Invalid salary values cleaned: "
        f"{invalid_salary_count}"
    )

    logger.info(
        f"Invalid salary ranges cleaned: "
        f"{invalid_range_count}"
    )

    logger.info(
        f"Final records: {len(df)}"
    )

    logger.info(
        f"Cleaned data saved to {file_path}"
    )

    return file_path


if __name__ == "__main__":
    from etl.config import PROCESSED_DATA_DIR

    clean_data(
        PROCESSED_DATA_DIR / "jobs_clean.csv"
    )