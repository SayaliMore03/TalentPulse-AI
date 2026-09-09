import pandas as pd

from etl.config import PROCESSED_DATA_DIR
from etl.utils.logger import get_logger

logger = get_logger(__name__)


def load_fact_jobs(connection):
    """
    Load job postings into fact_jobs.
    """
    file_path = PROCESSED_DATA_DIR / "jobs_clean.csv"

    logger.info(f"Reading processed data from {file_path}")

    df = pd.read_csv(file_path)

    cursor = connection.cursor(dictionary=True)

    inserted_count = 0

    for _, job in df.iterrows():

        # Get company_id
        cursor.execute(
            """
            SELECT company_id
            FROM dim_company
            WHERE company_name = %s
            """,
            (job["company"],),
        )
        company = cursor.fetchone()

        # Get location_id
        cursor.execute(
            """
            SELECT location_id
            FROM dim_location
            WHERE location_name = %s
            """,
            (job["location"],),
        )
        location = cursor.fetchone()

        # Get category_id
        cursor.execute(
            """
            SELECT category_id
            FROM dim_category
            WHERE category_name = %s
            """,
            (job["category"],),
        )
        category = cursor.fetchone()

        # Get date_id
        job_date = pd.to_datetime(job["created"]).date()

        cursor.execute(
            """
            SELECT date_id
            FROM dim_date
            WHERE full_date = %s
            """,
            (job_date,),
        )
        date = cursor.fetchone()

        if not location or not category or not date:
           logger.warning(
        f"Skipping job {job['job_id']} because a required dimension lookup failed."
    )
           continue
        cursor.execute(
            """
            INSERT IGNORE INTO fact_jobs (
                job_id,
                title,
                company_id,
                location_id,
                category_id,
                date_id,
                salary_min,
                salary_max,
                contract_type,
                contract_time,
                description,
                redirect_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                job["job_id"],
                job["title"],
                company["company_id"] if company else None,
                location["location_id"],
                category["category_id"],
                date["date_id"],
                job["salary_min"],
                job["salary_max"],
                job["contract_type"],
                job["contract_time"],
                job["description"],
                job["redirect_url"],
            ),
        )

        if cursor.rowcount == 1:
            inserted_count += 1

    connection.commit()

    logger.info(f"Inserted {inserted_count} new jobs.")