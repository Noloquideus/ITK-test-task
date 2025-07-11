from abc import ABC, abstractmethod
from src.infrastructure.database.models.wallet import Wallet


class IWalletService(ABC):

    @abstractmethod
    async def create(self) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def deposit(self, wallet_id: str, value: float) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def withdraw(self, wallet_id: str, value: float) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def get_wallet(self, wallet_id: str) -> Wallet:
        raise NotImplementedError

