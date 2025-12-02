# BigQuery Data Pipeline - Recruitment Test

A simple data ingestion and transformation pipeline using Google BigQuery, Python, and SQL.

## Project Overview

This pipeline demonstrates:
- **Data Ingestion**: Load CSV/JSON files into BigQuery
- **Data Transformation**: Multi-stage transformations (Raw → Staging → Production)
- **Data Quality**: Automated quality checks
- **Flexible Execution**: Run via Python or SQL

## Architecture

```
data/              # Source data files (CSV, JSON)
  └── *.csv
  
sql/               # SQL transformation scripts
  ├── staging_*.sql      # Raw → Staging transformations
  ├── prod_*.sql         # Staging → Production transformations
  └── data_quality_checks.sql
  
src/               # Python pipeline code
  ├── config.py          # Configuration management
  ├── bigquery_client.py # BigQuery wrapper
  ├── ingestion.py       # Data ingestion module
  ├── transformation.py  # Transformation module
  └── pipeline.py        # Main orchestrator
  
config/            # Configuration files
tests/             # Unit tests
```

### Data Flow

```
Raw Files (CSV/JSON) → raw_data (BigQuery) → staging (cleaned) → production (aggregated)
```

## Prerequisites

- Python 3.8+
- Google Cloud Platform account
- BigQuery API enabled
- Service account with BigQuery permissions

## Setup Instructions

### 1. Clone or Download This Repository

```powershell
cd C:\Users\ingdb\OneDrive\Documents\0x\recruitment
```

### 2. Install Dependencies

```powershell
cd data-engineer-recruitment-test
pip install -r requirements.txt
```

### 3. Configure GCP Credentials

Create a service account in GCP and download the JSON key file.

### 4. Set Environment Variables

Copy `.env.example` to `.env` and update with your values:

```powershell
cp .env.example .env
```

Edit `.env`:
```
GCP_PROJECT_ID=your-project-id
GCP_CREDENTIALS_PATH=path/to/your/service-account.json
BQ_DATASET_RAW=raw_data
BQ_DATASET_STAGING=staging
BQ_DATASET_PROD=production
BQ_LOCATION=US
```

### 5. Prepare Your Data

Place your CSV or JSON files in the `data/` directory. The pipeline will automatically:
- Detect file types
- Create tables named after the filename
- Load data into the `raw_data` dataset

## Usage

### Run Full Pipeline (Ingestion + Transformation)

```powershell
python -m src.pipeline full
```

### Run Individual Steps

**Ingestion only:**
```powershell
python -m src.pipeline ingest
```

**Transformation only:**
```powershell
python -m src.pipeline transform
```

### Run Specific Modules

**Ingestion:**
```powershell
python -m src.ingestion
```

**Transformation:**
```powershell
python -m src.transformation
```

## Customization

### Adding New Transformations

1. **Staging transformations** (Raw → Staging):
   - Create `sql/staging_<table_name>.sql`
   - The pipeline will automatically detect and run it

2. **Production transformations** (Staging → Production):
   - Create `sql/prod_<table_name>.sql`
   - The pipeline will automatically detect and run it

### Example SQL Files

See the example files in `sql/`:
- `staging_sample_table.sql` - Data cleaning and standardization
- `prod_daily_metrics.sql` - Aggregations and business logic
- `data_quality_checks.sql` - Quality validation queries

## Data Quality Checks

Run quality checks:
```powershell
# Execute in BigQuery Console or via bq CLI
bq query --use_legacy_sql=false < sql/data_quality_checks.sql
```

## Testing

Run tests:
```powershell
pytest tests/
```

## Project Structure Details

### Python Modules

- **config.py**: Environment configuration and project paths
- **bigquery_client.py**: BigQuery operations wrapper
- **ingestion.py**: File-to-BigQuery loading
- **transformation.py**: SQL-based transformations
- **pipeline.py**: Main orchestrator with CLI

### SQL Conventions

- `staging_*.sql`: Clean and validate raw data
- `prod_*.sql`: Create production-ready datasets
- Use `${GCP_PROJECT_ID}` placeholder in SQL (auto-replaced by Python)

## Common Tasks

### View BigQuery Tables

```powershell
# List datasets
bq ls

# List tables in a dataset
bq ls raw_data

# Query a table
bq query --use_legacy_sql=false "SELECT * FROM raw_data.your_table LIMIT 10"
```

### Clear and Reload Data

The pipeline uses `WRITE_TRUNCATE` by default, so running ingestion again will replace existing data.

## Troubleshooting

**Authentication errors:**
- Verify `GCP_CREDENTIALS_PATH` in `.env`
- Ensure service account has BigQuery permissions

**Import errors:**
- Ensure you're in the project root directory
- Use `python -m src.pipeline` (module syntax)

**No data found:**
- Check that files are in `data/` directory
- Verify file extensions (.csv or .json)
- Check logs for ingestion errors

## Optional: Airflow Integration

To add Airflow orchestration:

1. Install Airflow:
```powershell
pip install apache-airflow apache-airflow-providers-google
```

2. Create DAG in `dags/` directory (example structure provided in comments)

## License

MIT License - See LICENSE file for details

## Contact

For questions about this recruitment test, contact the hiring team.
