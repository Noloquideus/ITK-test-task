from decimal import Decimal
from src.application.abstractions.i_wallet_repository import IWalletRepository
from src.application.contracts.i_wallet_service import IWalletService
from src.infrastructure.database.models.wallet import Wallet
from src.infrastructure.logger import Logger
from src.application.exceptions import (
    WalletNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidWalletIdError,
    DatabaseError
)


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

        Raises:
            DatabaseError: If wallet creation fails
        """
        try:
            self._logger.info('Creating new wallet')
            wallet = await self._wallet_repository.create()
            self._logger.info(f'Wallet created successfully: {wallet.id}')
            return wallet
        except DatabaseError:
            self._logger.error('Database error during wallet creation')
            raise
        except Exception as e:
            self._logger.error(f'Unexpected error during wallet creation: {e}')
            raise DatabaseError(f'Wallet creation failed: {e}')

    async def deposit(self, wallet_id: str, amount: Decimal) -> Wallet:
        """
        Deposit money into a wallet.

        Args:
            wallet_id: The wallet ID to deposit into
            amount: The amount to deposit

        Returns:
            Wallet: The updated wallet entity

        Raises:
            InvalidAmountError: If amount is not positive
            InvalidWalletIdError: If wallet ID format is invalid
            WalletNotFoundError: If wallet is not found
            DatabaseError: If deposit operation fails
        """
        try:
            self._logger.info(f'Depositing {amount} to wallet {wallet_id}')
            wallet = await self._wallet_repository.deposit(wallet_id, amount)
            self._logger.info(f'Deposit successful: wallet {wallet.id}, new balance: {wallet.balance}')
            return wallet
        except (InvalidAmountError, InvalidWalletIdError, WalletNotFoundError):
            # Re-raise domain exceptions without wrapping
            raise
        except Exception as e:
            self._logger.error(f'Unexpected error during deposit: {e}')
            raise DatabaseError(f'Deposit operation failed: {e}')

    async def withdraw(self, wallet_id: str, amount: Decimal) -> Wallet:
        """
        Withdraw money from a wallet.

        Args:
            wallet_id: The wallet ID to withdraw from
            amount: The amount to withdraw

        Returns:
            Wallet: The updated wallet entity

        Raises:
            InvalidAmountError: If amount is not positive
            InvalidWalletIdError: If wallet ID format is invalid
            WalletNotFoundError: If wallet is not found
            InsufficientFundsError: If wallet has insufficient funds
            DatabaseError: If withdraw operation fails
        """
        try:
            self._logger.info(f'Withdrawing {amount} from wallet {wallet_id}')
            wallet = await self._wallet_repository.withdraw(wallet_id, amount)
            self._logger.info(f'Withdraw successful: wallet {wallet.id}, new balance: {wallet.balance}')
            return wallet
        except (InvalidAmountError, InvalidWalletIdError, WalletNotFoundError, InsufficientFundsError):
            # Re-raise domain exceptions without wrapping
            raise
        except Exception as e:
            self._logger.error(f'Unexpected error during withdraw: {e}')
            raise DatabaseError(f'Withdraw operation failed: {e}')

    async def get_wallet(self, wallet_id: str) -> Wallet:
        """
        Retrieve a wallet by its ID.

        Args:
            wallet_id: The wallet ID to retrieve

        Returns:
            Wallet: The wallet entity

        Raises:
            InvalidWalletIdError: If wallet ID format is invalid
            WalletNotFoundError: If wallet is not found
            DatabaseError: If retrieval operation fails
        """
        try:
            self._logger.info(f'Getting wallet with ID: {wallet_id}')
            wallet = await self._wallet_repository.get_wallet(wallet_id=wallet_id)
            self._logger.info(f'Wallet retrieved successfully: {wallet.id}')
            return wallet
        except (InvalidWalletIdError, WalletNotFoundError):
            # Re-raise domain exceptions without wrapping
            raise
        except Exception as e:
            self._logger.error(f'Unexpected error during wallet retrieval: {e}')
            raise DatabaseError(f'Wallet retrieval failed: {e}')
