from src.application.abstractions import IWalletRepository
from src.infrastructure.database.models.wallet import Wallet


class WalletRepository(IWalletRepository):

    async def create(self) -> Wallet:
        wallet = Wallet(balance=0.0)
        self._session.add(wallet)
        await self._session.commit()
        await self._session.refresh(wallet)

        self._logger.info(f'Wallet created with ID: {wallet.id}')
        return wallet

    async def deposit(self, wallet_id: str, value: float) -> Wallet:
        pass

    async def withdraw(self, wallet_id: str, value: float) -> Wallet:
        pass

    async def get_wallet(self, wallet_id: str) -> Wallet:
        pass
