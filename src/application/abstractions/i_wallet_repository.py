from abc import abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.contracts.i_wallet_service import IWalletService
from src.infrastructure.database.models.wallet import Wallet
from src.infrastructure.logger import Logger


class IWalletRepository(IWalletService):

    def __init__(self, session: AsyncSession, logger: Logger):
        self._session = session
        self._logger = logger


    @abstractmethod
    async def create(self) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def deposit(self, wallet_id: str, amount: float) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def withdraw(self, wallet_id: str, amount: float) -> Wallet:
        raise NotImplementedError

    @abstractmethod
    async def get_wallet(self, wallet_id: str) -> Wallet:
        raise NotImplementedError
