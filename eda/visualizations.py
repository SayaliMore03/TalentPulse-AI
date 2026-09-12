import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


DATA_PATH = Path("data/processed/jobs_clean.csv")
OUTPUT_DIR = Path("reports/figures")


def load_data():
    logger.info("Loading dataset from %s", DATA_PATH)

    df = pd.read_csv(DATA_PATH)

    df["created"] = pd.to_datetime(
        df["created"],
        errors="coerce",
        utc=True
    )

    logger.info("Dataset loaded successfully: %s rows", len(df))

    return df


def plot_jobs_by_location(df):
    location_counts = df["location"].value_counts().sort_values()

    plt.figure(figsize=(10, 6))
    location_counts.plot(kind="barh")

    plt.title("Number of Data Analyst Jobs by Location")
    plt.xlabel("Number of Jobs")
    plt.ylabel("Location")

    plt.tight_layout()

    output_path = OUTPUT_DIR / "jobs_by_location.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    logger.info("Saved: %s", output_path)


def plot_jobs_by_posting_date(df):
    daily_counts = (
        df.groupby(df["created"].dt.date)
        .size()
    )

    plt.figure(figsize=(10, 6))
    daily_counts.plot(kind="line", marker="o")

    plt.title("Jobs by Posting Date")
    plt.xlabel("Posting Date")
    plt.ylabel("Number of Jobs")

    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "jobs_by_posting_date.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    logger.info("Saved: %s", output_path)


def plot_missing_values(df):
    missing_percentage = df.isnull().mean() * 100

    missing_percentage = (
        missing_percentage[missing_percentage > 0]
        .sort_values()
    )

    plt.figure(figsize=(8, 5))
    missing_percentage.plot(kind="barh")

    plt.title("Missing Values by Column")
    plt.xlabel("Missing Percentage (%)")
    plt.ylabel("Column")

    plt.tight_layout()

    output_path = OUTPUT_DIR / "missing_values.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    logger.info("Saved: %s", output_path)


def plot_contract_time(df):
    contract_counts = (
        df["contract_time"]
        .fillna("Not Specified")
        .value_counts()
    )

    plt.figure(figsize=(8, 5))
    contract_counts.plot(kind="bar")

    plt.title("Contract Time Distribution")
    plt.xlabel("Contract Time")
    plt.ylabel("Number of Jobs")

    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "contract_time_distribution.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    logger.info("Saved: %s", output_path)


def main():
    logger.info("Starting visualization generation...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()

    plot_jobs_by_location(df)
    plot_jobs_by_posting_date(df)
    plot_missing_values(df)
    plot_contract_time(df)

    logger.info("All visualizations generated successfully.")


if __name__ == "__main__":
    main()