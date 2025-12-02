"""Main pipeline orchestrator."""

import argparse
import logging
from .config import Config
from .ingestion import DataIngestion
from .transformation import DataTransformation

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_ingestion():
    """Run data ingestion process."""
    logger.info("Starting data ingestion...")
    ingestion = DataIngestion()
    ingestion.ingest_directory(str(Config.DATA_DIR))
    logger.info("Data ingestion completed")


def run_transformation():
    """Run data transformation process."""
    logger.info("Starting data transformation...")
    transformation = DataTransformation()
    transformation.run_full_pipeline()
    logger.info("Data transformation completed")


def run_full_pipeline():
    """Run complete pipeline: ingestion + transformation."""
    logger.info("=" * 70)
    logger.info("STARTING FULL DATA PIPELINE")
    logger.info("=" * 70)
    
    try:
        # Step 1: Ingest data
        run_ingestion()
        
        # Step 2: Transform data
        run_transformation()
        
        logger.info("=" * 70)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


def main():
    """Main entry point with CLI arguments."""
    parser = argparse.ArgumentParser(description='BigQuery Data Pipeline')
    parser.add_argument(
        'action',
        choices=['ingest', 'transform', 'full'],
        help='Pipeline action to perform'
    )
    
    args = parser.parse_args()
    
    # Validate configuration
    Config.validate()
    
    # Run requested action
    if args.action == 'ingest':
        run_ingestion()
    elif args.action == 'transform':
        run_transformation()
    elif args.action == 'full':
        run_full_pipeline()


if __name__ == "__main__":
    main()
