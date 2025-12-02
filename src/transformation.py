"""Data transformation module using SQL and Python."""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
from .bigquery_client import BigQueryClient
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataTransformation:
    """Handle data transformations in BigQuery."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize transformation pipeline.
        
        Args:
            credentials_path: Optional path to GCP credentials
        """
        self.bq_client = BigQueryClient(credentials_path)
    
    def run_transformation(
        self,
        sql_file: str,
        destination_table: str,
        params: Optional[Dict[str, Any]] = None
    ) -> None:
        """Run a transformation from a SQL file.
        
        Args:
            sql_file: Path to SQL transformation file
            destination_table: Destination table (format: dataset.table)
            params: Optional parameters for the query
        """
        sql_path = Config.SQL_DIR / sql_file
        
        if not sql_path.exists():
            raise FileNotFoundError(f"SQL file not found: {sql_path}")
        
        logger.info(f"Running transformation: {sql_file}")
        logger.info(f"Destination: {destination_table}")
        
        self.bq_client.execute_query_from_file(
            sql_file=str(sql_path),
            destination_table=destination_table,
            params=params
        )
        
        # Get result table info
        dataset, table = destination_table.split('.')
        result_table = self.bq_client.get_table_info(dataset, table)
        logger.info(f"Transformation complete: {result_table.num_rows} rows in output")
    
    def run_staging_transformations(self) -> None:
        """Run all staging transformations (raw -> staging)."""
        logger.info("Running staging transformations...")
        
        staging_sqls = list(Config.SQL_DIR.glob("staging_*.sql"))
        
        for sql_file in staging_sqls:
            # Extract table name from filename (e.g., staging_orders.sql -> orders)
            table_name = sql_file.stem.replace("staging_", "")
            destination = f"{Config.BQ_DATASET_STAGING}.{table_name}"
            
            try:
                self.run_transformation(
                    sql_file=sql_file.name,
                    destination_table=destination
                )
            except Exception as e:
                logger.error(f"Error in staging transformation {sql_file.name}: {e}")
                raise
    
    def run_production_transformations(self) -> None:
        """Run all production transformations (staging -> production)."""
        logger.info("Running production transformations...")
        
        prod_sqls = list(Config.SQL_DIR.glob("prod_*.sql"))
        
        for sql_file in prod_sqls:
            # Extract table name from filename
            table_name = sql_file.stem.replace("prod_", "")
            destination = f"{Config.BQ_DATASET_PROD}.{table_name}"
            
            try:
                self.run_transformation(
                    sql_file=sql_file.name,
                    destination_table=destination
                )
            except Exception as e:
                logger.error(f"Error in production transformation {sql_file.name}: {e}")
                raise
    
    def run_full_pipeline(self) -> None:
        """Run the complete transformation pipeline (staging -> production)."""
        logger.info("=" * 60)
        logger.info("Starting full transformation pipeline")
        logger.info("=" * 60)
        
        try:
            self.run_staging_transformations()
            self.run_production_transformations()
            
            logger.info("=" * 60)
            logger.info("Pipeline completed successfully!")
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise


def main():
    """Example usage of transformation pipeline."""
    Config.validate()
    
    transformation = DataTransformation()
    transformation.run_full_pipeline()


if __name__ == "__main__":
    main()
