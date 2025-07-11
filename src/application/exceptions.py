class WalletError(Exception):
    """Base exception for all wallet-related errors."""
    pass


class WalletNotFoundError(WalletError):
    """Raised when a wallet with the specified ID is not found."""
    pass


class InsufficientFundsError(WalletError):
    """Raised when attempting to withdraw more money than available in the wallet."""
    pass


class InvalidAmountError(WalletError):
    """Raised when the operation amount is invalid (e.g., negative or zero)."""
    pass


class InvalidWalletIdError(WalletError):
    """Raised when the wallet ID format is invalid."""
    pass


class DatabaseError(WalletError):
    """Raised when a database operation fails."""
    pass
