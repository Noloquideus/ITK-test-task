import uuid
from contextlib import asynccontextmanager
from sqlalchemy import select
from src.application.abstractions import IWalletRepository
from src.infrastructure.database.models.wallet import Wallet
from src.application.exceptions import (
    WalletNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidWalletIdError,
    DatabaseError
)


class WalletRepository(IWalletRepository):
    """
    Repository implementation for wallet database operations.

    Provides methods for creating, retrieving, and modifying wallet entities
    with proper transaction handling and concurrency control.
    """


    async def create(self) -> Wallet:
        """
        Create a new wallet with zero balance.

        Returns:
            Wallet: The created wallet entity

        Raises:
            DatabaseError: If wallet creation fails
        """
        try:
            wallet = Wallet(balance=0.0)
            self._session.add(wallet)
            await self._session.commit()
            await self._session.refresh(wallet)

            self._logger.info(f'Wallet created with ID: {wallet.id}')
            return wallet
        except Exception as e:
            self._logger.error(f'Wallet creation failed: {e}')
            raise DatabaseError(f'Failed to create wallet: {e}')


    @asynccontextmanager
    async def _get_locked_wallet(self, wallet_id: str):
        """
        Get a wallet with row-level locking for concurrent operations.

        Args:
            wallet_id: The wallet ID to retrieve

        Yields:
            Wallet: The locked wallet entity

        Raises:
            InvalidWalletIdError: If wallet ID format is invalid
            WalletNotFoundError: If wallet is not found
        """
        try:
            wallet_uuid = uuid.UUID(wallet_id)
        except ValueError:
            raise InvalidWalletIdError(f'Invalid wallet ID format: {wallet_id}')

        query = select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()
        result = await self._session.execute(query)
        wallet = result.scalar_one_or_none()

        if wallet is None:
            raise WalletNotFoundError(f'Wallet with ID {wallet_id} not found')

        try:
            yield wallet
        finally:
            pass


    async def deposit(self, wallet_id: str, amount: float) -> Wallet:
        """
        Deposit money into a wallet.

        Args:
            wallet_id: The wallet ID to deposit into
            amount: The amount to deposit (must be positive)

        Returns:
            Wallet: The updated wallet entity

        Raises:
            InvalidAmountError: If amount is not positive
            InvalidWalletIdError: If wallet ID format is invalid
            WalletNotFoundError: If wallet is not found
            DatabaseError: If deposit operation fails
        """
        try:
            if amount <= 0:
                raise InvalidAmountError(f'Deposit amount must be positive: {amount}')

            async with self._get_locked_wallet(wallet_id) as wallet:
                wallet.balance += amount
                await self._session.commit()
                await self._session.refresh(wallet)

                self._logger.info(
                    f'Wallet {wallet.id} deposited: +{amount}, '
                    f'new balance: {wallet.balance}'
                )
                return wallet

        except (InvalidAmountError, InvalidWalletIdError, WalletNotFoundError):
            await self._session.rollback()
            raise
        except Exception as e:
            await self._session.rollback()
            self._logger.error(f'Unexpected deposit error: {str(e)}')
            raise DatabaseError(f'Deposit operation failed: {e}')


    async def withdraw(self, wallet_id: str, amount: float) -> Wallet:
        """
        Withdraw money from a wallet.

        Args:
            wallet_id: The wallet ID to withdraw from
            amount: The amount to withdraw (must be positive)

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
            if amount <= 0:
                raise InvalidAmountError(f'Withdraw amount must be positive: {amount}')

            async with self._get_locked_wallet(wallet_id) as wallet:
                if wallet.balance < amount:
                    raise InsufficientFundsError(
                        f'Insufficient funds: balance {wallet.balance}, '
                        f'requested {amount}'
                    )

                wallet.balance -= amount
                await self._session.commit()
                await self._session.refresh(wallet)

                self._logger.info(
                    f'Wallet {wallet.id} withdrawn: -{amount}, '
                    f'new balance: {wallet.balance}'
                )
                return wallet

        except (InvalidAmountError, InvalidWalletIdError, WalletNotFoundError, InsufficientFundsError):
            await self._session.rollback()
            raise
        except Exception as e:
            await self._session.rollback()
            self._logger.error(f'Unexpected withdraw error: {str(e)}')
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
        """
        try:
            wallet_uuid = uuid.UUID(wallet_id)
        except ValueError:
            self._logger.error(f'Invalid wallet ID: {wallet_id}')
            raise InvalidWalletIdError(f'Invalid wallet ID format: {wallet_id}')

        query = select(Wallet).where(Wallet.id == wallet_uuid)
        result = await self._session.execute(query)
        wallet = result.scalar_one_or_none()

        if wallet is None:
            self._logger.error(f'Wallet with ID {wallet_id} not found')
            raise WalletNotFoundError(f'Wallet with ID {wallet_id} not found')

        self._logger.info(f'Wallet retrieved: {wallet.id}')
        return wallet

