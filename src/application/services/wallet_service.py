from src.application.abstractions.i_wallet_repository import IWalletRepository
from src.application.contracts.i_wallet_service import IWalletService
from src.infrastructure.database.models.wallet import Wallet
from src.infrastructure.logger import Logger


class WalletService(IWalletService):

    def __init__(self, wallet_repository: IWalletRepository, logger: Logger):
        self._wallet_repository = wallet_repository
        self._logger = logger


    async def create(self) -> Wallet:
        try:
            self._logger.info('Creating new wallet')
            wallet = await self._wallet_repository.create()
            self._logger.info(f'Wallet created successfully: {wallet.id}')
            return wallet
        except Exception as e:
            self._logger.error(f'Wallet creation failed: {e}')
            raise e

    async def deposit(self, wallet_id: str, amount: float) -> Wallet:
        self._logger.info(f'Depositing {amount} to wallet {wallet_id}')
        wallet = await self._wallet_repository.deposit(wallet_id, amount)
        self._logger.info(f'Deposit successful: wallet {wallet.id}, new balance: {wallet.balance}')
        return wallet

    async def withdraw(self, wallet_id: str, amount: float) -> Wallet:
        self._logger.info(f'Withdrawing {amount} from wallet {wallet_id}')
        wallet = await self._wallet_repository.withdraw(wallet_id, amount)
        self._logger.info(f'Withdraw successful: wallet {wallet.id}, new balance: {wallet.balance}')
        return wallet

    async def get_wallet(self, wallet_id: str) -> Wallet:
        try:
            self._logger.info(f'Get wallet with wallet_id - {wallet_id}')
            wallet = await self._wallet_repository.get_wallet(wallet_id=wallet_id)
            self._logger.info(f'Wallet get successfully: {wallet.id}')
            return wallet

        except Exception as e:
            self._logger.error(f'Wallet creation failed: {e}')
            raise e
