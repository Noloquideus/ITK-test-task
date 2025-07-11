from enum import Enum


class Operation(str, Enum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
