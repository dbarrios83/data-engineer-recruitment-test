"""Data ingestion module for loading data into BigQuery."""

import logging
from pathlib import Path
from typing import Optional
from .bigquery_client import BigQueryClient
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataIngestion:
    """Handle data ingestion into BigQuery."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize ingestion pipeline.
        
        Args:
            credentials_path: Optional path to GCP credentials
        """
        self.bq_client = BigQueryClient(credentials_path)
        self._setup_datasets()
    
    def _setup_datasets(self):
        """Create required datasets if they don't exist."""
        logger.info("Setting up BigQuery datasets...")
        self.bq_client.create_dataset(Config.BQ_DATASET_RAW)
        self.bq_client.create_dataset(Config.BQ_DATASET_STAGING)
        self.bq_client.create_dataset(Config.BQ_DATASET_PROD)
    
    def ingest_csv(
        self,
        file_path: str,
        table_name: str,
        dataset: str = None
    ) -> None:
        """Ingest a CSV file into BigQuery.
        
        Args:
            file_path: Path to CSV file
            table_name: Target table name
            dataset: Target dataset (default: raw_data)
        """
        dataset = dataset or Config.BQ_DATASET_RAW
        
        logger.info(f"Ingesting {file_path} into {dataset}.{table_name}")
        
        self.bq_client.load_data_from_file(
            source_file=file_path,
            dataset_id=dataset,
            table_id=table_name,
            write_disposition="WRITE_TRUNCATE"
        )
        
        # Get table info
        table = self.bq_client.get_table_info(dataset, table_name)
        logger.info(f"Ingestion complete: {table.num_rows} rows loaded")
    
    def ingest_json(
        self,
        file_path: str,
        table_name: str,
        dataset: str = None
    ) -> None:
        """Ingest a JSON file into BigQuery.
        
        Args:
            file_path: Path to JSON file (newline-delimited)
            table_name: Target table name
            dataset: Target dataset (default: raw_data)
        """
        dataset = dataset or Config.BQ_DATASET_RAW
        
        logger.info(f"Ingesting {file_path} into {dataset}.{table_name}")
        
        self.bq_client.load_data_from_file(
            source_file=file_path,
            dataset_id=dataset,
            table_id=table_name,
            write_disposition="WRITE_TRUNCATE"
        )
        
        table = self.bq_client.get_table_info(dataset, table_name)
        logger.info(f"Ingestion complete: {table.num_rows} rows loaded")
    
    def ingest_directory(
        self,
        directory: str,
        file_pattern: str = "*.csv",
        dataset: str = None
    ) -> None:
        """Ingest all files matching pattern from a directory.
        
        Args:
            directory: Directory path
            file_pattern: File pattern to match (default: *.csv)
            dataset: Target dataset (default: raw_data)
        """
        dataset = dataset or Config.BQ_DATASET_RAW
        dir_path = Path(directory)
        
        files = list(dir_path.glob(file_pattern))
        logger.info(f"Found {len(files)} files matching {file_pattern}")
        
        for file_path in files:
            # Use filename (without extension) as table name
            table_name = file_path.stem
            
            if file_path.suffix == '.csv':
                self.ingest_csv(str(file_path), table_name, dataset)
            elif file_path.suffix == '.json':
                self.ingest_json(str(file_path), table_name, dataset)
            else:
                logger.warning(f"Unsupported file type: {file_path}")


def main():
    """Example usage of ingestion pipeline."""
    Config.validate()
    
    ingestion = DataIngestion()
    
    # Example: ingest all CSV files from data directory
    data_dir = Config.DATA_DIR
    if data_dir.exists():
        ingestion.ingest_directory(str(data_dir))
    else:
        logger.info(f"No data directory found at {data_dir}")
        logger.info("Place your CSV or JSON files in the data/ directory")


if __name__ == "__main__":
    main()
