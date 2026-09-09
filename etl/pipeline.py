from etl.extract import main as extract
from etl.transform import main as transform
from etl.clean import clean_data
from etl.validation import validate_data
from etl.load import load_to_database

from etl.utils.logger import get_logger

logger = get_logger(__name__)


def run_pipeline():
    """
    Run the complete TalentPulse AI ETL pipeline.
    """

    logger.info(
        "Starting TalentPulse AI ETL pipeline..."
    )

    # 1. Extract
    raw_file = extract()

    # 2. Transform
    processed_file = transform()

    # 3. Clean
    cleaned_file = clean_data(processed_file)

    # 4. Validate
    validate_data(cleaned_file)

    # 5. Load
    load_to_database()

    logger.info(
        "TalentPulse AI ETL pipeline completed successfully."
    )


if __name__ == "__main__":
    run_pipeline()