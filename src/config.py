"""Configuration management for the pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Pipeline configuration."""
    
    # GCP Settings
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_CREDENTIALS_PATH = os.getenv("GCP_CREDENTIALS_PATH")
    
    # BigQuery Settings
    BQ_DATASET_RAW = os.getenv("BQ_DATASET_RAW", "raw_data")
    BQ_DATASET_STAGING = os.getenv("BQ_DATASET_STAGING", "staging")
    BQ_DATASET_PROD = os.getenv("BQ_DATASET_PROD", "production")
    BQ_LOCATION = os.getenv("BQ_LOCATION", "US")
    
    # Project Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    SQL_DIR = PROJECT_ROOT / "sql"
    DATA_DIR = PROJECT_ROOT / "data"
    CONFIG_DIR = PROJECT_ROOT / "config"
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.GCP_PROJECT_ID:
            raise ValueError("GCP_PROJECT_ID must be set in environment variables")
        
        return True
