from decimal import Decimal, InvalidOperation
from fastapi import APIRouter, Path, status, Depends, HTTPException
from fastapi.params import Query
from src.application.contracts import IWalletService
from src.application.domain.operation_type import Operation
from src.application.services import get_wallet_service
from src.infrastructure.database.models.wallet import Wallet
from src.infrastructure.logger import get_logger, Logger
from src.presentation.schemas.wallet import WalletSchema
from src.application.exceptions import (
    WalletNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidWalletIdError,
    DatabaseError
)


wallets_router = APIRouter(prefix='/wallets', tags=['wallets'])


@wallets_router.post(path='/create', status_code=201, response_model=WalletSchema)
async def create_wallet(
        logger: Logger = Depends(get_logger),
        wallet_service: IWalletService = Depends(get_wallet_service)
):
    """
    Create a new wallet.

    Creates a new wallet with zero balance and returns the wallet information.

    Returns:
        WalletSchema: The created wallet information

    Raises:
        HTTPException: If wallet creation fails
    """
    try:
        wallet: Wallet = await wallet_service.create()
        logger.info(f'Wallet created: {wallet.id}')
        return WalletSchema(id=str(wallet.id), balance=wallet.balance)

    except DatabaseError as e:
        logger.error(f'Database error during wallet creation: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database operation failed')
    except Exception as e:
        logger.error(f'Unexpected error during wallet creation: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')


@wallets_router.post(path='/{wallet_id}/operation', status_code=status.HTTP_201_CREATED, response_model=WalletSchema)
async def wallet_operation(
        wallet_id: str = Path(title='Wallet ID'),
        amount: str = Query(title='Amount', description='Amount as decimal string (e.g., "100.50")'),
        operation_type: Operation = Query(title='Operation'),
        logger: Logger = Depends(get_logger),
        wallet_service: IWalletService = Depends(get_wallet_service)
):
    """
    Perform a wallet operation (deposit or withdraw).

    Executes a deposit or withdrawal operation on the specified wallet.

    Args:
        wallet_id: The wallet ID to perform the operation on
        amount: The amount for the operation as decimal string (must be positive)
        operation_type: The type of operation (DEPOSIT or WITHDRAW)

    Returns:
        WalletSchema: The updated wallet information

    Raises:
        HTTPException: If the operation fails for any reason
    """
    try:
        # Validate and convert amount string to Decimal
        try:
            amount_decimal = Decimal(amount)
            if amount_decimal <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Amount must be positive')
        except (InvalidOperation, ValueError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid amount format')
        
        if operation_type == Operation.DEPOSIT:
            wallet: Wallet = await wallet_service.deposit(wallet_id, amount_decimal)
        elif operation_type == Operation.WITHDRAW:
            wallet = await wallet_service.withdraw(wallet_id, amount_decimal)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid operation type')

        logger.info(f'Operation {operation_type.value} completed for wallet {wallet_id}')
        return WalletSchema(id=str(wallet.id), balance=wallet.balance)

    except InvalidWalletIdError as e:
        logger.error(f'Invalid wallet ID: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except WalletNotFoundError as e:
        logger.error(f'Wallet not found: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except InvalidAmountError as e:
        logger.error(f'Invalid amount: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except InsufficientFundsError as e:
        logger.error(f'Insufficient funds: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except DatabaseError as e:
        logger.error(f'Database error: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database operation failed')

    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')


@wallets_router.get(path='/{wallet_id}', status_code=status.HTTP_200_OK, response_model=WalletSchema)
async def get_wallet(
        wallet_id: str = Path(title='Wallet ID'),
        logger: Logger = Depends(get_logger),
        wallet_service: IWalletService = Depends(get_wallet_service)
):
    """
    Get wallet information by ID.

    Retrieves and returns the wallet information including balance and creation date.

    Args:
        wallet_id: The wallet ID to retrieve

    Returns:
        WalletSchema: The wallet information

    Raises:
        HTTPException: If the wallet is not found or other errors occur
    """
    try:
        wallet: Wallet = await wallet_service.get_wallet(wallet_id=wallet_id)
        logger.info(f'Wallet retrieved: {wallet.id}')
        return WalletSchema(id=str(wallet.id), balance=wallet.balance)

    except InvalidWalletIdError as e:
        logger.error(f'Invalid wallet ID: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except WalletNotFoundError as e:
        logger.error(f'Wallet not found: {e}')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except DatabaseError as e:
        logger.error(f'Database error: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database operation failed')

    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
