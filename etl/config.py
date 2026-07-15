# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Credentials (validated)
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY")

if not ADZUNA_APP_ID or not ADZUNA_API_KEY:
    raise RuntimeError("Missing Adzuna API credentials. Check your .env file.")

# API Configuration
BASE_URL = "https://api.adzuna.com/v1/api/jobs"
COUNTRY = "in"  # India

# Search Defaults
DEFAULT_SEARCH_KEYWORD = "Data Analyst"  # human-readable default
RESULTS_PER_PAGE = 20

# Data Paths
RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
ARCHIVE_DATA_DIR = Path("data/archive")

for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, ARCHIVE_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
