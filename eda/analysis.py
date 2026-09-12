import pandas as pd

from etl.config import PROCESSED_DATA_DIR
from etl.utils.logger import get_logger


logger = get_logger(__name__)


def load_data():
    """
    Load the cleaned jobs dataset.
    """

    file_path = PROCESSED_DATA_DIR / "jobs_clean.csv"

    logger.info(f"Loading dataset from {file_path}")

    df = pd.read_csv(file_path)

    logger.info("Dataset loaded successfully.")

    return df


def explore_dataset(df):
    """
    Display basic information about the dataset.
    """

    print("\n" + "=" * 50)
    print("DATASET OVERVIEW")
    print("=" * 50)

    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nFirst 5 Records:")
    print(df.head())

    print("\nData Types:")
    print(df.dtypes)

    print("\nDataset Information:")
    df.info()


def analyze_missing_values(df):
    """
    Analyze missing values in the dataset.
    """

    print("\n" + "=" * 50)
    print("MISSING VALUE ANALYSIS")
    print("=" * 50)

    missing_count = df.isnull().sum()

    missing_percentage = (
        df.isnull().mean() * 100
    ).round(2)

    missing_summary = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percentage": missing_percentage
    })

    missing_summary = missing_summary.sort_values(
        by="missing_count",
        ascending=False
    )

    print("\nMissing Values Summary:")
    print(missing_summary)

    print("\nColumns With Missing Values:")

    columns_with_missing = missing_summary[
        missing_summary["missing_count"] > 0
    ]

    print(columns_with_missing)


def analyze_duplicates(df):
    """
    Analyze duplicate records in the dataset.
    """

    print("\n" + "=" * 50)
    print("DUPLICATE ANALYSIS")
    print("=" * 50)

    duplicate_job_ids = df["job_id"].duplicated().sum()

    duplicate_rows = df.duplicated().sum()

    print(f"\nDuplicate job IDs: {duplicate_job_ids}")
    print(f"Duplicate complete rows: {duplicate_rows}")

    if duplicate_job_ids == 0:
        print("\nNo duplicate job IDs found.")

    if duplicate_rows == 0:
        print("No duplicate complete rows found.")



def analyze_categorical_columns(df):
    """
    Analyze unique values and frequency distributions
    for categorical columns.
    """

    print("\n" + "=" * 50)
    print("CATEGORICAL DATA ANALYSIS")
    print("=" * 50)

    categorical_columns = [
        "title",
        "company",
        "location",
        "category",
        "contract_type",
        "contract_time"
    ]

    for column in categorical_columns:
        print(f"\n--- {column.upper()} ---")

        print(f"Unique values: {df[column].nunique(dropna=True)}")

        print("\nValue counts:")
        print(df[column].value_counts(dropna=False).head(10))


def analyze_date_column(df):
    """
    Analyze job posting dates.
    """

    print("\n" + "=" * 50)
    print("DATE ANALYSIS")
    print("=" * 50)

    df["created"] = pd.to_datetime(df["created"], errors="coerce")

    print("\nDate Data Type:")
    print(df["created"].dtype)

    print("\nEarliest Job Posting:")
    print(df["created"].min())

    print("\nLatest Job Posting:")
    print(df["created"].max())

    print("\nMissing Dates:")
    print(df["created"].isnull().sum())

    print("\nJobs by Posting Date:")
    print(df["created"].dt.date.value_counts().sort_index())



def analyze_numerical_columns(df):
    """
    Analyze numerical columns in the dataset.
    """

    print("\n" + "=" * 50)
    print("NUMERICAL DATA ANALYSIS")
    print("=" * 50)

    numerical_columns = [
        "salary_min",
        "salary_max"
    ]

    print("\nSummary Statistics:")

    print(
        df[numerical_columns].describe()
    )

    print("\nMissing Salary Values:")

    print(
        df[numerical_columns].isnull().sum()
    )

    print("\nValid Salary Records:")

    valid_salary = df[
        df["salary_min"].notnull() &
        df["salary_max"].notnull()
    ]

    print(f"Records with complete salary information: {len(valid_salary)}")

    if len(valid_salary) > 0:
        print("\nSalary Statistics:")
        print(valid_salary[numerical_columns].describe())
    else:
        print("No complete salary records available for analysis.")



def analyze_text_columns(df):
    """
    Analyze text length in job descriptions.
    """

    print("\n" + "=" * 50)
    print("TEXT DATA ANALYSIS")
    print("=" * 50)

    df["description_length"] = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.len()
    )

    print("\nDescription Length Statistics:")
    print(df["description_length"].describe())

    print("\nShortest Description:")
    print(df["description_length"].min())

    print("\nLongest Description:")
    print(df["description_length"].max())

    print("\nAverage Description Length:")
    print(round(df["description_length"].mean(), 2))

    print("\nTop 5 Longest Job Descriptions:")
    print(
        df[
            ["job_id", "title", "description_length"]
        ]
        .sort_values(
            by="description_length",
            ascending=False
        )
        .head(5)
    )


def save_eda_summary(df):
    summary = {
        "total_jobs": len(df),
        "total_companies": df["company"].nunique(),
        "total_locations": df["location"].nunique(),
        "missing_salary_min": int(df["salary_min"].isna().sum()),
        "missing_salary_max": int(df["salary_max"].isna().sum()),
        "average_description_length": round(
            df["description"].fillna("").astype(str).str.len().mean(), 2
        ),
        "earliest_posting": df["created"].min(),
        "latest_posting": df["created"].max(),
    }

    summary_df = pd.DataFrame([summary])

    output_path = "data/processed/eda_summary.csv"
    summary_df.to_csv(output_path, index=False)

    print(f"\nEDA summary saved to: {output_path}")



def main():
    logger.info("Starting EDA...")

    df = load_data()

    explore_dataset(df)
    analyze_missing_values(df)
    analyze_duplicates(df)
    analyze_categorical_columns(df)
    analyze_date_column(df)
    analyze_numerical_columns(df)
    analyze_text_columns(df)
    save_eda_summary(df)
    logger.info("EDA summary saved successfully.")
    



if __name__ == "__main__":
    main()