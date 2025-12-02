"""Unit tests for data ingestion."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.ingestion import DataIngestion


class TestDataIngestion:
    """Test DataIngestion class."""
    
    @patch('src.ingestion.BigQueryClient')
    def test_ingestion_initialization(self, mock_bq_client):
        """Test ingestion initialization."""
        mock_client_instance = MagicMock()
        mock_bq_client.return_value = mock_client_instance
        
        ingestion = DataIngestion()
        assert ingestion.bq_client is not None


# Add more tests as needed
