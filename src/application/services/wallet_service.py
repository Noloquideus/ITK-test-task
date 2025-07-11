from src.application.abstractions.i_wallet_repository import IWalletRepository
from src.application.contracts.i_wallet_service import IWalletService
from src.infrastructure.database.models.wallet import Wallet
from src.infrastructure.logger import Logger


class WalletService(IWalletService):

    def __init__(self, wallet_repository: IWalletRepository, logger: Logger):
        self._wallet_repository = wallet_repository
        self._logger = logger


    async def create(self) -> Wallet:
        self._logger.info('Creating new wallet')
        wallet = await self._wallet_repository.create()
        self._logger.info(f'Wallet created successfully: {wallet.id}')
        return wallet

    async def deposit(self, wallet_id: str, value: float) -> Wallet:
        pass

    async def withdraw(self, wallet_id: str, value: float) -> Wallet:
        pass

    async def get_wallet(self, wallet_id: str) -> Wallet:
        pass
