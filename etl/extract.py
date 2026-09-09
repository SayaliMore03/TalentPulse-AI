import json
from datetime import datetime

import requests

from etl.config import (
    ADZUNA_APP_ID,
    ADZUNA_API_KEY,
    BASE_URL,
    COUNTRY,
    DEFAULT_SEARCH_KEYWORD,
    RAW_DATA_DIR,
    RESULTS_PER_PAGE,
)
from etl.utils.logger import get_logger

logger = get_logger(__name__)


def build_request_params() -> dict:
    """
    Build query parameters for the Adzuna API.
    """
    return {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": DEFAULT_SEARCH_KEYWORD,
    }


def fetch_jobs(params: dict) -> dict:
    """
    Fetch job postings from the Adzuna API with retry logic.
    """
    url = f"{BASE_URL}/{COUNTRY}/search/1"

    max_retries = 3

    for attempt in range(1, max_retries + 1):

        logger.info(
            f"Sending request to Adzuna API "
            f"(attempt {attempt}/{max_retries})..."
        )

        try:
            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            logger.info(
                "Successfully fetched job postings."
            )

            return response.json()

        except requests.exceptions.RequestException as e:

            logger.warning(
                f"API request failed on attempt "
                f"{attempt}: {e}"
            )

            if attempt == max_retries:
                logger.error(
                    "API request failed after all retries."
                )
                raise

            wait_time = 2 ** attempt

            logger.info(
                f"Retrying in {wait_time} seconds..."
            )

            import time
            time.sleep(wait_time)
    """
    Fetch job postings from the Adzuna API.
    """
    url = f"{BASE_URL}/{COUNTRY}/search/1"

    logger.info("Sending request to Adzuna API...")

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        logger.info("Successfully fetched job postings.")

        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise


def save_raw_json(data: dict) -> str:
    """
    Save the raw API response as a JSON file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = RAW_DATA_DIR / f"jobs_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    logger.info(f"Raw data saved to {file_path}")

    return str(file_path)


def main():
    logger.info("Starting extraction pipeline...")

    params = build_request_params()

    data = fetch_jobs(params)

    raw_file = save_raw_json(data)

    logger.info("Extraction completed successfully.")

    return raw_file


if __name__ == "__main__":
    main()