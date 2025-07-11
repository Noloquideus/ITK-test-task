"""
Unit tests for custom exceptions.

Tests the custom exception classes and their behavior.
"""
from src.application.exceptions import (
    WalletNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidWalletIdError,
    DatabaseError
)


class TestWalletNotFoundError:
    """Test cases for WalletNotFoundError."""

    def test_wallet_not_found_error_creation(self):
        """Test WalletNotFoundError creation."""
        # Arrange
        wallet_id = "non-existent-id"
        message = f"Wallet with ID {wallet_id} not found"

        # Act
        error = WalletNotFoundError(message)

        # Assert
        assert str(error) == message
        assert isinstance(error, Exception)

    def test_wallet_not_found_error_with_wallet_id(self):
        """Test WalletNotFoundError with wallet ID."""
        # Arrange
        wallet_id = "test-wallet-id"

        # Act
        error = WalletNotFoundError(f"Wallet with ID {wallet_id} not found")

        # Assert
        assert wallet_id in str(error)

    def test_wallet_not_found_error_inheritance(self):
        """Test WalletNotFoundError inheritance."""
        # Act
        error = WalletNotFoundError("Test message")

        # Assert
        assert isinstance(error, Exception)
        assert isinstance(error, WalletNotFoundError)


class TestInsufficientFundsError:
    """Test cases for InsufficientFundsError."""

    def test_insufficient_funds_error_creation(self):
        """Test InsufficientFundsError creation."""
        # Arrange
        balance = 100.0
        requested = 200.0
        message = f"Insufficient funds: balance {balance}, requested {requested}"

        # Act
        error = InsufficientFundsError(message)

        # Assert
        assert str(error) == message
        assert isinstance(error, Exception)

    def test_insufficient_funds_error_with_amounts(self):
        """Test InsufficientFundsError with balance and requested amounts."""
        # Arrange
        balance = 50.0
        requested = 100.0

        # Act
        error = InsufficientFundsError(f"Insufficient funds: balance {balance}, requested {requested}")

        # Assert
        assert str(balance) in str(error)
        assert str(requested) in str(error)

    def test_insufficient_funds_error_inheritance(self):
        """Test InsufficientFundsError inheritance."""
        # Act
        error = InsufficientFundsError("Test message")

        # Assert
        assert isinstance(error, Exception)
        assert isinstance(error, InsufficientFundsError)


class TestInvalidAmountError:
    """Test cases for InvalidAmountError."""

    def test_invalid_amount_error_creation(self):
        """Test InvalidAmountError creation."""
        # Arrange
        amount = -10.0
        message = f"Invalid amount: {amount}"

        # Act
        error = InvalidAmountError(message)

        # Assert
        assert str(error) == message
        assert isinstance(error, Exception)

    def test_invalid_amount_error_with_amount(self):
        """Test InvalidAmountError with specific amount."""
        # Arrange
        amount = 0.0

        # Act
        error = InvalidAmountError(f"Amount must be positive: {amount}")

        # Assert
        assert str(amount) in str(error)

    def test_invalid_amount_error_inheritance(self):
        """Test InvalidAmountError inheritance."""
        # Act
        error = InvalidAmountError("Test message")

        # Assert
        assert isinstance(error, Exception)
        assert isinstance(error, InvalidAmountError)


class TestInvalidWalletIdError:
    """Test cases for InvalidWalletIdError."""

    def test_invalid_wallet_id_error_creation(self):
        """Test InvalidWalletIdError creation."""
        # Arrange
        wallet_id = "invalid-uuid"
        message = f"Invalid wallet ID format: {wallet_id}"

        # Act
        error = InvalidWalletIdError(message)

        # Assert
        assert str(error) == message
        assert isinstance(error, Exception)

    def test_invalid_wallet_id_error_with_id(self):
        """Test InvalidWalletIdError with wallet ID."""
        # Arrange
        wallet_id = "not-a-uuid"

        # Act
        error = InvalidWalletIdError(f"Invalid wallet ID format: {wallet_id}")

        # Assert
        assert wallet_id in str(error)

    def test_invalid_wallet_id_error_inheritance(self):
        """Test InvalidWalletIdError inheritance."""
        # Act
        error = InvalidWalletIdError("Test message")

        # Assert
        assert isinstance(error, Exception)
        assert isinstance(error, InvalidWalletIdError)


class TestDatabaseError:
    """Test cases for DatabaseError."""

    def test_database_error_creation(self):
        """Test DatabaseError creation."""
        # Arrange
        operation = "create wallet"
        message = f"Database operation failed: {operation}"

        # Act
        error = DatabaseError(message)

        # Assert
        assert str(error) == message
        assert isinstance(error, Exception)

    def test_database_error_with_operation(self):
        """Test DatabaseError with specific operation."""
        # Arrange
        operation = "deposit"

        # Act
        error = DatabaseError(f"Failed to perform {operation} operation")

        # Assert
        assert operation in str(error)

    def test_database_error_inheritance(self):
        """Test DatabaseError inheritance."""
        # Act
        error = DatabaseError("Test message")

        # Assert
        assert isinstance(error, Exception)
        assert isinstance(error, DatabaseError)


class TestExceptionHierarchy:
    """Test cases for exception hierarchy and relationships."""

    def test_exception_hierarchy(self):
        """Test that all custom exceptions inherit from Exception."""
        exceptions = [
            WalletNotFoundError("test"),
            InsufficientFundsError("test"),
            InvalidAmountError("test"),
            InvalidWalletIdError("test"),
            DatabaseError("test")
        ]

        for exception in exceptions:
            assert isinstance(exception, Exception)

    def test_exception_uniqueness(self):
        """Test that exceptions are unique types."""
        exceptions = [
            WalletNotFoundError,
            InsufficientFundsError,
            InvalidAmountError,
            InvalidWalletIdError,
            DatabaseError
        ]

        for i, exc1 in enumerate(exceptions):
            for j, exc2 in enumerate(exceptions):
                if i != j:
                    assert exc1 != exc2

    def test_exception_messages(self):
        """Test that exceptions can have custom messages."""
        test_message = "Custom error message"

        wallet_error = WalletNotFoundError(test_message)
        funds_error = InsufficientFundsError(test_message)
        amount_error = InvalidAmountError(test_message)
        id_error = InvalidWalletIdError(test_message)
        db_error = DatabaseError(test_message)

        assert str(wallet_error) == test_message
        assert str(funds_error) == test_message
        assert str(amount_error) == test_message
        assert str(id_error) == test_message
        assert str(db_error) == test_message
