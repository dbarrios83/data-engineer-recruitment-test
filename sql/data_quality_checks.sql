-- Data quality checks example
-- Run this to validate your data quality

WITH quality_checks AS (
    SELECT
        'staging.sample_table' AS table_name,
        COUNT(*) AS total_rows,
        COUNT(DISTINCT id) AS unique_ids,
        SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS null_emails,
        SUM(CASE WHEN created_at IS NULL THEN 1 ELSE 0 END) AS null_dates,
        MIN(created_at) AS min_date,
        MAX(created_at) AS max_date
    FROM 
        `${GCP_PROJECT_ID}.staging.sample_table`
)

SELECT 
    *,
    CASE 
        WHEN total_rows = 0 THEN 'FAIL: No data'
        WHEN null_emails > total_rows * 0.1 THEN 'WARN: >10% null emails'
        WHEN total_rows != unique_ids THEN 'WARN: Duplicate IDs found'
        ELSE 'PASS'
    END AS quality_status
FROM 
    quality_checks;
