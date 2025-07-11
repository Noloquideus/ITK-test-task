import uuid
from sqlalchemy import select
from src.application.abstractions import IWalletRepository
from src.infrastructure.database.models.wallet import Wallet


class WalletRepository(IWalletRepository):


    async def create(self) -> Wallet:
        try:
            wallet = Wallet(balance=0.0)
            self._session.add(wallet)
            await self._session.commit()
            await self._session.refresh(wallet)

            self._logger.info(f'Wallet created with ID: {wallet.id}')
            return wallet
        except Exception as e:
            self._logger.error(f'Wallet creation failed: {e}')
            raise e

    async def deposit(self, wallet_id: str, value: float) -> Wallet:
        pass

    async def withdraw(self, wallet_id: str, value: float) -> Wallet:
        pass

    async def get_wallet(self, wallet_id: str) -> Wallet:

        try:
            wallet_uuid = uuid.UUID(wallet_id)
        except ValueError:
            self._logger.error(f'Invalid wallet ID: {wallet_id}')
            raise ValueError(f'Invalid wallet ID format: {wallet_id}')

        query = select(Wallet).where(Wallet.id == wallet_uuid)
        result = await self._session.execute(query)
        wallet = result.scalar_one_or_none()

        if wallet is None:
            self._logger.error(f'Wallet with ID {wallet_id} not found')
            raise ValueError(f'Wallet with ID {wallet_id} not found')

        self._logger.info(f'Wallet retrieved: {wallet.id}')
        return wallet

