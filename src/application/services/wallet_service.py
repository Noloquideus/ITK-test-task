from decimal import Decimal
from src.application.abstractions.i_wallet_repository import IWalletRepository
from src.application.contracts.i_wallet_service import IWalletService
from src.infrastructure.database.models.wallet import Wallet
from src.infrastructure.logger import Logger


class WalletService(IWalletService):
    """
    Service layer for wallet operations.

    Provides business logic for wallet creation, deposits, withdrawals,
    and retrieval operations with proper logging.
    """

    def __init__(self, wallet_repository: IWalletRepository, logger: Logger):
        """
        Initialize the wallet service.

        Args:
            wallet_repository: Repository for wallet data access
            logger: Logger instance for operation logging
        """
        self._wallet_repository = wallet_repository
        self._logger = logger


    async def create(self) -> Wallet:
        """
        Create a new wallet with zero balance.

        Returns:
            Wallet: The created wallet entity
        """
        try:
            self._logger.info('Creating new wallet')
            wallet = await self._wallet_repository.create()
            self._logger.info(f'Wallet created successfully: {wallet.id}')
            return wallet
        except Exception as e:
            self._logger.error(f'Wallet creation failed: {e}')
            raise e

    async def deposit(self, wallet_id: str, amount: Decimal) -> Wallet:
        """
        Deposit money into a wallet.

        Args:
            wallet_id: The wallet ID to deposit into
            amount: The amount to deposit

        Returns:
            Wallet: The updated wallet entity
        """
        self._logger.info(f'Depositing {amount} to wallet {wallet_id}')
        wallet = await self._wallet_repository.deposit(wallet_id, amount)
        self._logger.info(f'Deposit successful: wallet {wallet.id}, new balance: {wallet.balance}')
        return wallet

    async def withdraw(self, wallet_id: str, amount: Decimal) -> Wallet:
        """
        Withdraw money from a wallet.

        Args:
            wallet_id: The wallet ID to withdraw from
            amount: The amount to withdraw

        Returns:
            Wallet: The updated wallet entity
        """
        self._logger.info(f'Withdrawing {amount} from wallet {wallet_id}')
        wallet = await self._wallet_repository.withdraw(wallet_id, amount)
        self._logger.info(f'Withdraw successful: wallet {wallet.id}, new balance: {wallet.balance}')
        return wallet

    async def get_wallet(self, wallet_id: str) -> Wallet:
        """
        Retrieve a wallet by its ID.

        Args:
            wallet_id: The wallet ID to retrieve

        Returns:
            Wallet: The wallet entity
        """
        try:
            self._logger.info(f'Get wallet with wallet_id - {wallet_id}')
            wallet = await self._wallet_repository.get_wallet(wallet_id=wallet_id)
            self._logger.info(f'Wallet get successfully: {wallet.id}')
            return wallet

        except Exception as e:
            self._logger.error(f'Wallet creation failed: {e}')
            raise e
