# TalentPulse-AI — Exploratory Data Analysis Report

## Dataset Overview

- Total job postings: 20
- Total companies: 20
- Total locations: 9
- Primary job title: Data Analyst
- Date range: September 1, 2026 to September 9, 2026

## Location Insights

The dataset contains job postings from multiple Indian locations.

Most frequent locations:

- India: 6 jobs
- Hyderabad, Telangana: 3 jobs
- Bangalore, Karnataka: 3 jobs
- Mumbai, Maharashtra: 2 jobs
- Noida, Ghaziabad: 2 jobs

## Category Insights

- IT Jobs: 19 postings
- PR, Advertising & Marketing Jobs: 1 posting

The dataset is primarily focused on IT-related Data Analyst opportunities.

## Contract Insights

- Full-time jobs: 9
- Contract jobs: 1
- Contract time not specified: 11

## Salary Insights

Salary analysis could not be performed because all 20 records have missing salary_min and salary_max values.

This is an important data-quality limitation.

## Text Insights

- Average description length: 499 characters
- Shortest description: 480 characters
- Longest description: 500 characters

Most descriptions are exactly 500 characters, suggesting that descriptions may have been truncated during extraction.

## Data Quality Summary

| Column | Missing Percentage |
|---|---:|
| salary_min | 100% |
| salary_max | 100% |
| contract_type | 95% |
| contract_time | 55% |

No duplicate job IDs or duplicate complete rows were found.

## Conclusion

The dataset is suitable for initial job-market exploration and dashboard development. However, salary analysis and detailed skill extraction will require improved salary coverage and longer, untruncated job descriptions.