from abc import ABC, abstractmethod
from decimal import Decimal
from src.infrastructure.database.models.wallet import Wallet


class IWalletService(ABC):

    @abstractmethod
    async def create(self) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def deposit(self, wallet_id: str, amount: Decimal) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def withdraw(self, wallet_id: str, amount: Decimal) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def get_wallet(self, wallet_id: str) -> Wallet:
        raise NotImplementedError

