from fastapi import Depends
from src.application.abstractions import IWalletRepository
from src.application.contracts import IWalletService
from src.application.services.wallet_service import WalletService
from src.infrastructure.database.repositories import get_wallet_repository
from src.infrastructure.logger import get_logger, Logger


async def get_wallet_service(wallet_repository: IWalletRepository = Depends(get_wallet_repository), logger: Logger = Depends(get_logger)) -> IWalletService:
    yield WalletService(wallet_repository=wallet_repository, logger=logger)
