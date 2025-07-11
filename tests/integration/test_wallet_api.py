"""
Integration tests for Wallet API.

Tests the complete API endpoints including request/response handling,
error scenarios, and documentation accessibility.
"""

import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from src.main import app
from src.infrastructure.database.models.wallet import Wallet


class TestWalletAPI:
    """Test cases for Wallet API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def mock_wallet(self):
        """Create mock wallet for testing."""
        return Wallet(
            id="test-wallet-id",
            balance=Decimal("100.00"),
            created_at="2025-01-01T00:00:00Z"
        )

    def test_openapi_schema_accessible(self, client):
        """Test that OpenAPI schema is accessible."""
        # Act
        response = client.get("/openapi.json")

        # Assert
        assert response.status_code == 200
        assert "openapi" in response.json()
