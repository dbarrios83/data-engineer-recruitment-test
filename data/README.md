# Sample data directory

Place your CSV or JSON files here for ingestion.

## Example CSV Format

```csv
id,name,email,created_at
1,John Doe,john@example.com,2024-01-01 10:00:00
2,Jane Smith,jane@example.com,2024-01-02 11:30:00
```

## Example JSON Format (newline-delimited)

```json
{"id": 1, "name": "John Doe", "email": "john@example.com", "created_at": "2024-01-01 10:00:00"}
{"id": 2, "name": "Jane Smith", "email": "jane@example.com", "created_at": "2024-01-02 11:30:00"}
```

The pipeline will automatically detect files and create BigQuery tables with names matching the filename (without extension).
