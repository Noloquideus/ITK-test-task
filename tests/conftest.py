"""
Pytest configuration and fixtures for wallet API tests.

This file contains shared fixtures and configuration for all test modules.
"""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from src.infrastructure.database.models.wallet import Wallet
from src.infrastructure.database.repositories.wallet_repostiory import WalletRepository
from src.application.services.wallet_service import WalletService



@pytest.fixture
def mock_wallet():
    """
    Create a mock wallet instance for testing.

    Returns:
        Wallet: Mock wallet with test data
    """
    return Wallet(
        id="test-wallet-id",
        balance=Decimal("100.00"),
        created_at="2025-01-01T00:00:00Z"
    )


@pytest.fixture
def mock_session():
    """
    Create a mock database session for testing.

    Returns:
        AsyncMock: Mock async database session
    """
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    # Use regular Mock for synchronous methods
    session.add = Mock()
    return session


@pytest.fixture
def repository(mock_session):
    """
    Create a repository instance with mock session for testing.

    Returns:
        WalletRepository: Repository instance with mock session
    """
    return WalletRepository(mock_session, Mock())


@pytest.fixture
def mock_wallet_repository():
    """
    Create a mock wallet repository for testing.

    Returns:
        AsyncMock: Mock wallet repository
    """
    return AsyncMock(spec=WalletRepository)


@pytest.fixture
def mock_wallet_service():
    """
    Create a mock wallet service for testing.

    Returns:
        AsyncMock: Mock wallet service
    """
    return AsyncMock(spec=WalletService)


@pytest.fixture
def mock_logger():
    """
    Create a mock logger for testing.

    Returns:
        Mock: Mock logger
    """
    return Mock()


@pytest.fixture
def sample_wallet_data():
    """
    Sample wallet data for testing.

    Returns:
        dict: Sample wallet data
    """
    return {
        "id": "test-wallet-id",
        "balance": Decimal("100.00"),
        "created_at": "2025-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_deposit_data():
    """
    Sample deposit data for testing.

    Returns:
        dict: Sample deposit data
    """
    return {
        "wallet_id": "test-wallet-id",
        "amount": Decimal("50.00")
    }


@pytest.fixture
def sample_withdraw_data():
    """
    Sample withdraw data for testing.

    Returns:
        dict: Sample withdraw data
    """
    return {
        "wallet_id": "test-wallet-id",
        "amount": Decimal("25.00")
    }
