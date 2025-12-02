-- Example production transformation: Create aggregated metrics
-- This transforms data from staging dataset to production dataset
-- Filename pattern: prod_*.sql

-- Replace with your actual business logic
SELECT
    DATE(created_at) AS date,
    COUNT(DISTINCT id) AS total_records,
    COUNT(DISTINCT CASE WHEN data_quality_flag = 'valid' THEN id END) AS valid_records,
    COUNT(DISTINCT CASE WHEN data_quality_flag = 'invalid' THEN id END) AS invalid_records,
    CURRENT_TIMESTAMP() AS processed_at
FROM 
    `${GCP_PROJECT_ID}.staging.sample_table`
GROUP BY 
    DATE(created_at)
ORDER BY 
    date DESC;
