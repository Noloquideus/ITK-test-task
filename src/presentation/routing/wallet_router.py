from fastapi import APIRouter, Path, status, Depends
from src.application.contracts import IWalletService
from src.application.domain.operation_type import Operation
from src.application.services import get_wallet_service
from src.infrastructure.database.models.wallet import Wallet
from src.infrastructure.logger import get_logger, Logger
from src.presentation.schemas.wallet import WalletSchema


wallets_router = APIRouter(prefix='/wallets', tags=['wallets'])


@wallets_router.post(path='/create', status_code=201, response_model=WalletSchema)
async def create_wallet(
        logger: Logger = Depends(get_logger),
        wallet_service: IWalletService = Depends(get_wallet_service)
):
    wallet: Wallet = await wallet_service.create()
    logger.info(f'Wallet created: {wallet.id}')
    return WalletSchema(id=str(wallet.id), balance=wallet.balance)


@wallets_router.post(path='/{wallet_id}/operation', status_code=status.HTTP_201_CREATED, response_model=WalletSchema)
async def wallet_operation(
        wallet_id: str = Path(title='Wallet ID'),
        operation: Operation = Path(title='Operation'),
        logger: Logger = Depends(get_logger),
        wallet_service: IWalletService = Depends(get_wallet_service)
):
    pass


@wallets_router.get(path='/{wallet_id}', status_code=status.HTTP_200_OK, response_model=WalletSchema)
async def get_wallet(
        wallet_id: str = Path(title='Wallet ID'),
        logger: Logger = Depends(get_logger),
        wallet_service: IWalletService = Depends(get_wallet_service)
):
    pass
