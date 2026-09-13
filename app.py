import logging
from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATA_PATH = Path("data/processed/jobs_clean.csv")


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="TalentPulse-AI",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
    }

    [data-testid="stMetric"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 1rem;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }

    .insight-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #1f2937;
        border: 1px solid #374151;
        min-height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():
    logger.info("Loading dashboard dataset from %s", DATA_PATH)

    df = pd.read_csv(DATA_PATH)

    df["created"] = pd.to_datetime(
        df["created"],
        errors="coerce",
        utc=True
    )

    logger.info("Dataset loaded successfully: %s rows", len(df))

    return df


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📊 TalentPulse-AI")
st.subheader("Data Analyst Job Market Dashboard")

st.markdown(
    "Explore job opportunities, locations, companies, and hiring trends."
)


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

try:
    df = load_data()

except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()


# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("Filters")

locations = sorted(
    df["location"]
    .dropna()
    .unique()
    .tolist()
)

selected_locations = st.sidebar.multiselect(
    "Select Location",
    options=locations,
    default=locations
)


categories = sorted(
    df["category"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=categories,
    default=categories
)


# --------------------------------------------------
# Filter Data
# --------------------------------------------------

filtered_df = df[
    df["location"].isin(selected_locations)
    & df["category"].isin(selected_categories)
]


# Handle Empty Filters

if filtered_df.empty:
    st.warning(
        "No jobs match the selected filters. "
        "Please select at least one location and category."
    )
    st.stop()


# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Jobs",
        len(filtered_df)
    )


with col2:
    st.metric(
        "Companies",
        filtered_df["company"].nunique()
    )


with col3:
    st.metric(
        "Locations",
        filtered_df["location"].nunique()
    )


with col4:
    full_time_jobs = (
        filtered_df["contract_time"]
        .eq("full_time")
        .sum()
    )

    st.metric(
        "Full-Time Jobs",
        int(full_time_jobs)
    )


st.divider()


# --------------------------------------------------
# Salary Data Quality Warning
# --------------------------------------------------

salary_missing_percentage = (
    filtered_df["salary_min"].isna().mean() * 100
)


if salary_missing_percentage == 100:
    st.warning(
        "Salary information is unavailable for all currently filtered job postings."
    )

elif salary_missing_percentage > 50:
    st.warning(
        f"Salary information is missing for "
        f"{salary_missing_percentage:.0f}% of currently filtered job postings."
    )


# --------------------------------------------------
# Charts — Location and Category
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:
    st.subheader("Jobs by Location")

    location_counts = (
        filtered_df["location"]
        .value_counts()
        .sort_values(ascending=True)
    )

    st.bar_chart(
        location_counts,
        horizontal=True
    )


with col2:
    st.subheader("Jobs by Category")

    category_counts = (
        filtered_df["category"]
        .value_counts()
    )

    st.bar_chart(category_counts)


st.divider()


# --------------------------------------------------
# Charts — Posting Date and Contract Time
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:
    st.subheader("Jobs by Posting Date")

    daily_counts = (
        filtered_df
        .groupby(filtered_df["created"].dt.date)
        .size()
    )

    st.line_chart(daily_counts)


with col2:
    st.subheader("Contract Time Distribution")

    contract_counts = (
        filtered_df["contract_time"]
        .fillna("Not Specified")
        .value_counts()
    )

    st.bar_chart(contract_counts)


st.divider()


# --------------------------------------------------
# Data Quality Summary
# --------------------------------------------------

st.subheader("Data Quality Summary")

missing_data = (
    filtered_df.isnull()
    .sum()
    .reset_index()
)

missing_data.columns = [
    "Column",
    "Missing Values"
]

missing_data["Missing Percentage"] = (
    missing_data["Missing Values"]
    / len(filtered_df)
    * 100
).round(2)

missing_data = missing_data[
    missing_data["Missing Values"] > 0
]

st.dataframe(
    missing_data,
    use_container_width=True,
    hide_index=True
)


st.divider()


# --------------------------------------------------
# Quick Insights
# --------------------------------------------------

st.subheader("Quick Insights")

insight_col1, insight_col2, insight_col3 = st.columns(3)


with insight_col1:

    top_location = (
        filtered_df["location"]
        .value_counts()
        .idxmax()
    )

    top_location_count = (
        filtered_df["location"]
        .value_counts()
        .max()
    )

    st.info(
        f"Most common location:\n\n"
        f"**{top_location}** ({top_location_count} jobs)"
    )


with insight_col2:

    top_category = (
        filtered_df["category"]
        .value_counts()
        .idxmax()
    )

    st.info(
        f"Leading category:\n\n"
        f"**{top_category}**"
    )


with insight_col3:

    avg_description_length = (
        filtered_df["description"]
        .fillna("")
        .astype(str)
        .str.len()
        .mean()
    )

    st.info(
        f"Average description length:\n\n"
        f"**{avg_description_length:.0f} characters**"
    )


st.divider()


# --------------------------------------------------
# Raw Job Listings
# --------------------------------------------------

st.subheader("Job Listings")

display_columns = [
    "job_id",
    "title",
    "company",
    "location",
    "category",
    "contract_time",
    "created",
    "redirect_url"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "TalentPulse-AI | Built with Python, Pandas, and Streamlit"
)