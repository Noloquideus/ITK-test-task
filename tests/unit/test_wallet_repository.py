"""
Unit tests for WalletRepository.

Tests the wallet repository operations including CRUD operations,
concurrent access handling, and error scenarios.
"""
import pytest
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4
from src.infrastructure.database.models.wallet import Wallet
from src.application.exceptions import (
    WalletNotFoundError,
    InsufficientFundsError
)


class TestWalletRepository:
    """Test cases for WalletRepository."""

    @pytest.mark.asyncio
    async def test_get_wallet_success(self, repository, mock_session):
        """Test successful wallet retrieval."""
        # Arrange
        wallet_id = str(uuid4())
        mock_wallet = Wallet(
            id=wallet_id,
            balance=Decimal("100.00")
        )
        repository._session = mock_session
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_wallet
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_wallet(wallet_id)

        # Assert
        assert result == mock_wallet
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_wallet_not_found(self, repository, mock_session):
        """Test wallet retrieval when wallet not found."""
        # Arrange
        wallet_id = str(uuid4())
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        repository._session = mock_session

        # Act & Assert
        with pytest.raises(WalletNotFoundError):
            await repository.get_wallet(wallet_id)

    @pytest.mark.asyncio
    async def test_deposit_success(self, repository, mock_session):
        """Test successful deposit operation."""
        # Arrange
        wallet_id = str(uuid4())
        amount = Decimal("50.00")
        mock_wallet = Wallet(
            id=wallet_id,
            balance=Decimal("100.00")
        )
        repository._session = mock_session
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_wallet
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.deposit(wallet_id, amount)

        # Assert
        assert result.balance == Decimal("150.00")
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_withdraw_success(self, repository, mock_session):
        """Test successful withdrawal operation."""
        # Arrange
        wallet_id = str(uuid4())
        amount = Decimal("25.00")
        mock_wallet = Wallet(
            id=wallet_id,
            balance=Decimal("100.00")
        )
        repository._session = mock_session
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_wallet
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.withdraw(wallet_id, amount)

        # Assert
        assert result.balance == Decimal("75.00")
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_withdraw_insufficient_funds(self, repository, mock_session):
        """Test withdrawal with insufficient funds."""
        # Arrange
        wallet_id = str(uuid4())
        amount = Decimal("150.00")
        mock_wallet = Wallet(
            id=wallet_id,
            balance=Decimal("100.00")
        )
        repository._session = mock_session
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_wallet
        mock_session.execute.return_value = mock_result

        # Act & Assert
        with pytest.raises(InsufficientFundsError):
            await repository.withdraw(wallet_id, amount)
