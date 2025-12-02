-- Example staging transformation: Clean and standardize raw data
-- This transforms data from raw_data dataset to staging dataset
-- Filename pattern: staging_*.sql

-- Replace with your actual raw table and transformation logic
SELECT
    -- Add your column transformations here
    CAST(id AS INT64) AS id,
    TRIM(name) AS name,
    LOWER(email) AS email,
    PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', created_at) AS created_at,
    -- Add data quality checks
    CASE 
        WHEN email IS NULL OR email = '' THEN 'invalid'
        ELSE 'valid'
    END AS data_quality_flag
FROM 
    `${GCP_PROJECT_ID}.raw_data.sample_table`
WHERE
    -- Filter out invalid records
    id IS NOT NULL
    AND created_at IS NOT NULL;
