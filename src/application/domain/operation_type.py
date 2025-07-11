from enum import Enum


class Operation(str, Enum):
    """
    Enumeration of wallet operation types.

    Attributes:
        DEPOSIT: Add money to the wallet
        WITHDRAW: Remove money from the wallet
    """
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
