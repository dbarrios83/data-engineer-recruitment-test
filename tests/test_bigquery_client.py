"""Unit tests for BigQuery client."""

import pytest
from unittest.mock import Mock, patch
from src.bigquery_client import BigQueryClient


class TestBigQueryClient:
    """Test BigQueryClient class."""
    
    @patch('src.bigquery_client.bigquery.Client')
    def test_client_initialization(self, mock_client):
        """Test client initialization without credentials."""
        client = BigQueryClient()
        assert client.client is not None
    
    @patch('src.bigquery_client.bigquery.Client')
    @patch('src.bigquery_client.service_account.Credentials')
    def test_client_with_credentials(self, mock_creds, mock_client):
        """Test client initialization with credentials."""
        mock_creds.from_service_account_file.return_value = Mock()
        client = BigQueryClient(credentials_path="test.json")
        assert client.client is not None


# Add more tests as needed
