from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.application.exceptions import (
    WalletNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidWalletIdError,
    DatabaseError,
    WalletError
)


async def wallet_not_found_handler(_request: Request, exc: WalletNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'detail': str(exc),
            'error_code': 'WALLET_NOT_FOUND',
            'error_type': 'not_found'
        }
    )


async def insufficient_funds_handler(_request: Request, exc: InsufficientFundsError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'detail': str(exc),
            'error_code': 'INSUFFICIENT_FUNDS',
            'error_type': 'validation_error'
        }
    )


async def invalid_amount_handler(_request: Request, exc: InvalidAmountError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'detail': str(exc),
            'error_code': 'INVALID_AMOUNT',
            'error_type': 'validation_error'
        }
    )


async def invalid_wallet_id_handler(_request: Request, exc: InvalidWalletIdError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'detail': str(exc),
            'error_code': 'INVALID_WALLET_ID',
            'error_type': 'validation_error'
        }
    )


async def database_error_handler(_request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'detail': f'Database operation failed: {str(exc)}',
            'error_code': 'DATABASE_ERROR',
            'error_type': 'server_error'
        }
    )


async def wallet_error_handler(_request: Request, exc: WalletError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'detail': f'Wallet operation failed: {str(exc)}',
            'error_code': 'WALLET_ERROR',
            'error_type': 'server_error'
        }
    )
