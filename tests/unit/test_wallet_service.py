"""
Unit tests for WalletService.

Tests the business logic layer including wallet operations,
validation, and error handling.
"""
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from src.application.services.wallet_service import WalletService
from src.infrastructure.database.models.wallet import Wallet
from src.application.exceptions import (
    WalletNotFoundError,
    InsufficientFundsError
)


class TestWalletService:
    """Test cases for WalletService."""

    @pytest.mark.asyncio
    async def test_create_wallet_success(self, mock_wallet_repository):
        """Test successful wallet creation."""
        # Arrange
        mock_wallet = Wallet(
            id="test-wallet-id",
            balance=Decimal("0.00")
        )
        mock_wallet_repository.create.return_value = mock_wallet
        service = WalletService(mock_wallet_repository, Mock())

        # Act
        result = await service.create()

        # Assert
        assert result == mock_wallet
        mock_wallet_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_wallet_failure(self, mock_wallet_repository):
        """Test wallet creation failure."""
        # Arrange
        mock_wallet_repository.create.side_effect = Exception("Database error")
        service = WalletService(mock_wallet_repository, Mock())

        # Act & Assert
        with pytest.raises(Exception):
            await service.create()

    @pytest.mark.asyncio
    async def test_get_wallet_success(self, mock_wallet_repository):
        """Test successful wallet retrieval."""
        # Arrange
        wallet_id = "test-wallet-id"
        mock_wallet = Wallet(
            id=wallet_id,
            balance=Decimal("100.00")
        )
        mock_wallet_repository.get_wallet.return_value = mock_wallet
        service = WalletService(mock_wallet_repository, Mock())

        # Act
        result = await service.get_wallet(wallet_id)

        # Assert
        assert result == mock_wallet
        mock_wallet_repository.get_wallet.assert_called_once_with(wallet_id=wallet_id)

    @pytest.mark.asyncio
    async def test_get_wallet_not_found(self, mock_wallet_repository):
        """Test wallet retrieval when wallet not found."""
        # Arrange
        wallet_id = "test-wallet-id"
        mock_wallet_repository.get_wallet.side_effect = WalletNotFoundError("Wallet not found")
        service = WalletService(mock_wallet_repository, Mock())

        # Act & Assert
        with pytest.raises(WalletNotFoundError):
            await service.get_wallet(wallet_id)

    @pytest.mark.asyncio
    async def test_deposit_success(self, mock_wallet_repository):
        """Test successful deposit operation."""
        # Arrange
        wallet_id = "test-wallet-id"
        amount = Decimal("50.00")
        mock_wallet = Wallet(
            id=wallet_id,
            balance=Decimal("150.00")
        )
        mock_wallet_repository.deposit.return_value = mock_wallet
        service = WalletService(mock_wallet_repository, Mock())

        # Act
        result = await service.deposit(wallet_id, amount)

        # Assert
        assert result == mock_wallet
        mock_wallet_repository.deposit.assert_called_once_with(wallet_id, amount)

    @pytest.mark.asyncio
    async def test_withdraw_success(self, mock_wallet_repository):
        """Test successful withdrawal operation."""
        # Arrange
        wallet_id = "test-wallet-id"
        amount = Decimal("25.00")
        mock_wallet = Wallet(
            id=wallet_id,
            balance=Decimal("75.00")
        )
        mock_wallet_repository.withdraw.return_value = mock_wallet
        service = WalletService(mock_wallet_repository, Mock())

        # Act
        result = await service.withdraw(wallet_id, amount)

        # Assert
        assert result == mock_wallet
        mock_wallet_repository.withdraw.assert_called_once_with(wallet_id, amount)

    @pytest.mark.asyncio
    async def test_withdraw_insufficient_funds(self, mock_wallet_repository):
        """Test withdrawal with insufficient funds."""
        # Arrange
        wallet_id = "test-wallet-id"
        amount = Decimal("200.00")
        mock_wallet_repository.withdraw.side_effect = InsufficientFundsError("Insufficient funds")
        service = WalletService(mock_wallet_repository, Mock())

        # Act & Assert
        with pytest.raises(InsufficientFundsError):
            await service.withdraw(wallet_id, amount)
