import logging
from pathlib import Path

import pandas as pd
import streamlit as st


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


DATA_PATH = Path("data/processed/jobs_clean.csv")


@st.cache_data
def load_data():
    logger.info("Loading dashboard dataset from %s", DATA_PATH)

    df = pd.read_csv(DATA_PATH)

    df["created"] = pd.to_datetime(
        df["created"],
        errors="coerce",
        utc=True
    )

    return df


st.set_page_config(
    page_title="TalentPulse-AI",
    page_icon="📊",
    layout="wide"
)


st.title("📊 TalentPulse-AI")
st.subheader("Data Analyst Job Market Dashboard")

st.markdown(
    "Explore job opportunities, locations, companies, and hiring trends."
)


try:
    df = load_data()

except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()


# Sidebar filters

st.sidebar.header("Filters")

locations = sorted(df["location"].dropna().unique().tolist())

selected_locations = st.sidebar.multiselect(
    "Select Location",
    options=locations,
    default=locations
)

categories = sorted(df["category"].dropna().unique().tolist())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=categories,
    default=categories
)


filtered_df = df[
    df["location"].isin(selected_locations)
    & df["category"].isin(selected_categories)
]


# KPI Cards

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jobs", len(filtered_df))

with col2:
    st.metric("Companies", filtered_df["company"].nunique())

with col3:
    st.metric("Locations", filtered_df["location"].nunique())

with col4:
    full_time_jobs = (
        filtered_df["contract_time"]
        .eq("full_time")
        .sum()
    )

    st.metric("Full-Time Jobs", int(full_time_jobs))


st.divider()


# Charts

col1, col2 = st.columns(2)

with col1:
    st.subheader("Jobs by Location")

    location_counts = (
        filtered_df["location"]
        .value_counts()
        .sort_values(ascending=True)
    )

    st.bar_chart(location_counts)


with col2:
    st.subheader("Jobs by Category")

    category_counts = filtered_df["category"].value_counts()

    st.bar_chart(category_counts)


st.divider()


col1, col2 = st.columns(2)

with col1:
    st.subheader("Jobs by Location")

    location_counts = (
        filtered_df["location"]
        .value_counts()
        .sort_values(ascending=True)
    )

    st.bar_chart(location_counts, horizontal=True)

with col2:
    st.subheader("Jobs by Category")

    category_counts = filtered_df["category"].value_counts()

    st.bar_chart(category_counts)

st.divider()


# Data Quality Section

st.subheader("Data Quality Summary")

missing_data = (
    filtered_df.isnull()
    .sum()
    .reset_index()
)

missing_data.columns = ["Column", "Missing Values"]

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


# Raw Data

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


st.caption("TalentPulse-AI | Built with Python, Pandas, and Streamlit")