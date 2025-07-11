class WalletError(Exception):
    pass


class WalletNotFoundError(WalletError):
    pass


class InsufficientFundsError(WalletError):
    pass


class InvalidAmountError(WalletError):
    pass


class InvalidWalletIdError(WalletError):
    pass


class DatabaseError(WalletError):
    pass
