import json

import pandas as pd

from etl.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from etl.utils.logger import get_logger

logger = get_logger(__name__)


def get_latest_raw_file():
    """
    Returns the most recently created raw JSON file.
    """
    json_files = sorted(RAW_DATA_DIR.glob("jobs_*.json"))

    if not json_files:
        raise FileNotFoundError("No raw JSON files found.")

    return json_files[-1]


def load_raw_data(file_path):
    """
    Load raw JSON data.
    """
    logger.info(f"Loading raw data from {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_jobs(data):
    """
    Flatten nested JSON into a tabular structure.
    """
    jobs = []

    for job in data["results"]:

        jobs.append({
            "job_id": job.get("id"),
            "title": job.get("title"),

            "company":
                job.get("company", {}).get("display_name"),

            "location":
                job.get("location", {}).get("display_name"),

            "category":
                job.get("category", {}).get("label"),

            "salary_min":
                job.get("salary_min"),

            "salary_max":
                job.get("salary_max"),

            "contract_type":
                job.get("contract_type"),

            "contract_time":
                job.get("contract_time"),

            "created":
                job.get("created"),

            "description":
                job.get("description"),

            "redirect_url":
                job.get("redirect_url"),
        })

    return pd.DataFrame(jobs)


def save_processed_data(df):
    """
    Save transformed data as CSV.
    """
    output_path = PROCESSED_DATA_DIR / "jobs_clean.csv"

    df.to_csv(output_path, index=False)

    logger.info(
        f"Processed data saved to {output_path}"
    )

    return output_path


def main():

    raw_file = get_latest_raw_file()

    data = load_raw_data(raw_file)

    df = transform_jobs(data)

    processed_file = save_processed_data(df)

    return processed_file


if __name__ == "__main__":
    main()