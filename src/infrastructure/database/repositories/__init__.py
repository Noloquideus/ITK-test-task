from fastapi.params import Depends
from src.application.abstractions import IWalletRepository
from src.infrastructure.database.database import async_session_maker
from src.infrastructure.database.repositories.wallet_repostiory import WalletRepository
from src.infrastructure.logger import get_logger, Logger


async def get_wallet_repository(logger: Logger = Depends(get_logger)) -> IWalletRepository:
    async with async_session_maker() as session:
        yield WalletRepository(session=session, logger=logger)
