-- 1. Total number of job postings
SELECT COUNT(*) AS total_jobs
FROM fact_jobs;

-- 2. Number of jobs by company
SELECT
    c.company_name,
    COUNT(*) AS job_count
FROM fact_jobs f
JOIN dim_company c
    ON f.company_id = c.company_id
GROUP BY c.company_name
ORDER BY job_count DESC;

-- 3. Number of jobs by location
SELECT
    l.location_name,
    COUNT(*) AS job_count
FROM fact_jobs f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.location_name
ORDER BY job_count DESC;


-- 4. Number of jobs by category
SELECT
    c.category_name,
    COUNT(*) AS job_count
FROM fact_jobs f
JOIN dim_category c
    ON f.category_id = c.category_id
GROUP BY c.category_name
ORDER BY job_count DESC;


-- 5. Salary availability
SELECT
    COUNT(*) AS total_jobs,
    COUNT(salary_min) AS jobs_with_salary,
    COUNT(*) - COUNT(salary_min) AS jobs_without_salary,
    ROUND(
        COUNT(salary_min) * 100.0 / COUNT(*),
        2
    ) AS salary_disclosure_percentage
FROM fact_jobs;


-- 6. Salary statistics
SELECT
    COUNT(*) AS jobs_with_salary,
    ROUND(AVG(salary_min), 2) AS avg_min_salary,
    ROUND(AVG(salary_max), 2) AS avg_max_salary,
    MIN(salary_min) AS lowest_min_salary,
    MAX(salary_max) AS highest_max_salary
FROM fact_jobs
WHERE salary_min IS NOT NULL
  AND salary_max IS NOT NULL;

  
-- 7. Jobs by contract type
SELECT
    f.contract_type,
    COUNT(*) AS job_count
FROM fact_jobs f
GROUP BY f.contract_type
ORDER BY job_count DESC;

-- 8. Jobs by contract time
SELECT
    f.contract_time,
    COUNT(*) AS job_count
FROM fact_jobs f
GROUP BY f.contract_time
ORDER BY job_count DESC;


-- 9. Jobs by posting date
SELECT
    d.full_date,
    COUNT(*) AS job_count
FROM fact_jobs f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY d.full_date
ORDER BY d.full_date;


-- 11. Average salary by location
SELECT
    l.location_name,
    COUNT(*) AS jobs_with_salary,
    ROUND(AVG(f.salary_min), 2) AS avg_min_salary,
    ROUND(AVG(f.salary_max), 2) AS avg_max_salary
FROM fact_jobs f
JOIN dim_location l
    ON f.location_id = l.location_id
WHERE f.salary_min IS NOT NULL
  AND f.salary_max IS NOT NULL
GROUP BY l.location_name
HAVING COUNT(*) >= 2
ORDER BY avg_max_salary DESC;


-- 12. Average salary by company
SELECT
    c.company_name,
    COUNT(*) AS jobs_with_salary,
    ROUND(AVG(f.salary_min), 2) AS avg_min_salary,
    ROUND(AVG(f.salary_max), 2) AS avg_max_salary
FROM fact_jobs f
JOIN dim_company c
    ON f.company_id = c.company_id
WHERE f.salary_min IS NOT NULL
  AND f.salary_max IS NOT NULL
GROUP BY c.company_name
HAVING COUNT(*) >= 2
ORDER BY avg_max_salary DESC;


-- 13. Average salary by category
SELECT
    c.category_name,
    COUNT(*) AS jobs_with_salary,
    ROUND(AVG(f.salary_min), 2) AS avg_min_salary,
    ROUND(AVG(f.salary_max), 2) AS avg_max_salary
FROM fact_jobs f
JOIN dim_category c
    ON f.category_id = c.category_id
WHERE f.salary_min IS NOT NULL
  AND f.salary_max IS NOT NULL
GROUP BY c.category_name
HAVING COUNT(*) >= 2
ORDER BY avg_max_salary DESC;


-- 14. Salary range by job
SELECT
    f.job_id,
    f.title,
    f.salary_min,
    f.salary_max,
    ROUND(f.salary_max - f.salary_min, 2) AS salary_range
FROM fact_jobs f
WHERE f.salary_min IS NOT NULL
  AND f.salary_max IS NOT NULL
ORDER BY salary_range DESC;


-- 15. Jobs by location and category
SELECT
    l.location_name,
    c.category_name,
    COUNT(*) AS job_count
FROM fact_jobs f
JOIN dim_location l
    ON f.location_id = l.location_id
JOIN dim_category c
    ON f.category_id = c.category_id
GROUP BY
    l.location_name,
    c.category_name
ORDER BY
    job_count DESC;


-- 16. Salary disclosure by category
SELECT
    c.category_name,
    COUNT(*) AS total_jobs,
    COUNT(f.salary_min) AS jobs_with_salary,
    ROUND(
        COUNT(f.salary_min) * 100.0 / COUNT(*),
        2
    ) AS salary_disclosure_percentage
FROM fact_jobs f
JOIN dim_category c
    ON f.category_id = c.category_id
GROUP BY c.category_name
ORDER BY salary_disclosure_percentage DESC;


-- 17. Location demand and salary disclosure
SELECT
    l.location_name,
    COUNT(*) AS total_jobs,
    COUNT(f.salary_min) AS jobs_with_salary,
    ROUND(
        COUNT(f.salary_min) * 100.0 / COUNT(*),
        2
    ) AS salary_disclosure_percentage
FROM fact_jobs f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.location_name
ORDER BY total_jobs DESC;

