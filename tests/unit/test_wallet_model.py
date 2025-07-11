"""
Unit tests for Wallet model.

Tests the Wallet database model functionality including creation,
validation, and operations.
"""
from decimal import Decimal
from datetime import datetime, UTC
from src.infrastructure.database.models.wallet import Wallet


class TestWalletModel:
    """Test cases for Wallet model."""

    def test_wallet_creation(self):
        """Test wallet creation with valid data."""
        # Arrange
        wallet_id = "test-wallet-id"
        balance = Decimal("100.00")
        created_at = datetime.now(UTC)

        # Act
        wallet = Wallet(
            id=wallet_id,
            balance=balance,
            created_at=created_at
        )

        # Assert
        assert wallet.id == wallet_id
        assert wallet.balance == balance
        assert wallet.created_at == created_at

    def test_wallet_balance_decimal(self):
        """Test that balance is always Decimal."""
        # Arrange
        wallet = Wallet(
            id="test-wallet-id",
            balance=Decimal("123.45")
        )

        # Assert
        assert isinstance(wallet.balance, Decimal)
        assert wallet.balance == Decimal("123.45")

    def test_wallet_table_name(self):
        """Test wallet table name."""
        # Arrange
        wallet = Wallet(
            id="test-wallet-id"
        )

        # Assert
        assert wallet.__tablename__ == "wallets"

    def test_wallet_column_mapping(self):
        """Test wallet column mapping."""
        # Arrange
        wallet = Wallet(
            id="test-wallet-id"
        )

        # Assert
        assert hasattr(wallet, 'id')
        assert hasattr(wallet, 'balance')
        assert hasattr(wallet, 'created_at')
