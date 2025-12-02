"""BigQuery client wrapper for pipeline operations."""

from google.cloud import bigquery
from google.oauth2 import service_account
from typing import Optional, List, Dict, Any
import logging
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BigQueryClient:
    """Wrapper for Google BigQuery client with common operations."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize BigQuery client.
        
        Args:
            credentials_path: Path to service account JSON file
        """
        if credentials_path or Config.GCP_CREDENTIALS_PATH:
            creds_path = credentials_path or Config.GCP_CREDENTIALS_PATH
            credentials = service_account.Credentials.from_service_account_file(creds_path)
            self.client = bigquery.Client(
                credentials=credentials,
                project=Config.GCP_PROJECT_ID
            )
        else:
            # Use application default credentials
            self.client = bigquery.Client(project=Config.GCP_PROJECT_ID)
        
        logger.info(f"BigQuery client initialized for project: {Config.GCP_PROJECT_ID}")
    
    def create_dataset(self, dataset_id: str, location: str = None) -> bigquery.Dataset:
        """Create a BigQuery dataset if it doesn't exist.
        
        Args:
            dataset_id: Dataset ID
            location: Dataset location (default from config)
            
        Returns:
            BigQuery Dataset object
        """
        dataset_ref = f"{Config.GCP_PROJECT_ID}.{dataset_id}"
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location or Config.BQ_LOCATION
        
        try:
            dataset = self.client.create_dataset(dataset, exists_ok=True)
            logger.info(f"Dataset {dataset_id} created or already exists")
            return dataset
        except Exception as e:
            logger.error(f"Error creating dataset {dataset_id}: {e}")
            raise
    
    def load_data_from_file(
        self,
        source_file: str,
        dataset_id: str,
        table_id: str,
        schema: Optional[List[bigquery.SchemaField]] = None,
        write_disposition: str = "WRITE_TRUNCATE"
    ) -> bigquery.LoadJob:
        """Load data from a file into BigQuery.
        
        Args:
            source_file: Path to source file (CSV, JSON, etc.)
            dataset_id: Target dataset ID
            table_id: Target table ID
            schema: Table schema (optional, can be auto-detected)
            write_disposition: WRITE_TRUNCATE, WRITE_APPEND, or WRITE_EMPTY
            
        Returns:
            Load job object
        """
        table_ref = f"{Config.GCP_PROJECT_ID}.{dataset_id}.{table_id}"
        
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = write_disposition
        
        # Auto-detect schema if not provided
        if schema:
            job_config.schema = schema
        else:
            job_config.autodetect = True
        
        # Determine source format from file extension
        if source_file.endswith('.csv'):
            job_config.source_format = bigquery.SourceFormat.CSV
            job_config.skip_leading_rows = 1
        elif source_file.endswith('.json'):
            job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        
        with open(source_file, "rb") as source:
            job = self.client.load_table_from_file(
                source,
                table_ref,
                job_config=job_config
            )
        
        job.result()  # Wait for job to complete
        logger.info(f"Loaded {job.output_rows} rows into {table_ref}")
        return job
    
    def execute_query(
        self,
        query: str,
        destination_table: Optional[str] = None,
        write_disposition: str = "WRITE_TRUNCATE"
    ) -> bigquery.QueryJob:
        """Execute a SQL query.
        
        Args:
            query: SQL query string
            destination_table: Optional destination table (format: dataset.table)
            write_disposition: WRITE_TRUNCATE, WRITE_APPEND, or WRITE_EMPTY
            
        Returns:
            Query job object
        """
        job_config = bigquery.QueryJobConfig()
        
        if destination_table:
            table_ref = f"{Config.GCP_PROJECT_ID}.{destination_table}"
            job_config.destination = table_ref
            job_config.write_disposition = write_disposition
        
        query_job = self.client.query(query, job_config=job_config)
        query_job.result()  # Wait for completion
        
        logger.info(f"Query executed successfully")
        if destination_table:
            logger.info(f"Results written to {destination_table}")
        
        return query_job
    
    def execute_query_from_file(
        self,
        sql_file: str,
        destination_table: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> bigquery.QueryJob:
        """Execute a SQL query from a file.
        
        Args:
            sql_file: Path to SQL file
            destination_table: Optional destination table
            params: Optional parameters to substitute in query
            
        Returns:
            Query job object
        """
        with open(sql_file, 'r') as f:
            query = f.read()
        
        # Simple parameter substitution
        if params:
            for key, value in params.items():
                query = query.replace(f"${{{key}}}", str(value))
        
        return self.execute_query(query, destination_table)
    
    def get_table_info(self, dataset_id: str, table_id: str) -> bigquery.Table:
        """Get table metadata.
        
        Args:
            dataset_id: Dataset ID
            table_id: Table ID
            
        Returns:
            Table object with metadata
        """
        table_ref = f"{Config.GCP_PROJECT_ID}.{dataset_id}.{table_id}"
        table = self.client.get_table(table_ref)
        
        logger.info(f"Table {table_ref}: {table.num_rows} rows, {table.num_bytes} bytes")
        return table
