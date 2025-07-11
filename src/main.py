from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.infrastructure.logger import logger
from src.presentation.middleware.trace_id import TraceIDMiddleware
from src.presentation.routing.wallet_router import wallets_router
from src.presentation.exception_handlers import (
    wallet_not_found_handler,
    insufficient_funds_handler,
    invalid_amount_handler,
    invalid_wallet_id_handler,
    database_error_handler,
    wallet_error_handler
)
from src.application.exceptions import (
    WalletNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidWalletIdError,
    DatabaseError,
    WalletError
)
from src.settings import settings


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager.

    Handles application startup and shutdown events with proper logging.
    """
    logger.info('API Started')
    yield
    logger.info('API Stopped')


app: FastAPI = FastAPI(
    redoc_url=None,
    docs_url=None,
    lifespan=lifespan,
    title='ITK test task',
    version='1.0.0',
    description='',
    license_info={
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT',
    }
)

# Initialize HTTP Basic authentication
security = HTTPBasic(description='Basic Authentication for AndNowIT API')

# Function to verify user credentials
async def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Validate user credentials for API documentation access.

    Args:
        credentials: HTTP Basic authentication credentials

    Raises:
        HTTPException: If credentials are invalid
    """
    correct_username = settings.DOCS_USERNAME  # Username
    correct_password = settings.DOCS_PASSWORD  # Password hash

    if credentials.username != correct_username or not credentials.password == correct_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

app_router = APIRouter(prefix='/api/v1')
app_router.include_router(wallets_router)

app.include_router(app_router)

# Added middleware
app.add_middleware(TraceIDMiddleware, logger=logger)

# Register exception handlers
app.add_exception_handler(WalletNotFoundError, wallet_not_found_handler)
app.add_exception_handler(InsufficientFundsError, insufficient_funds_handler)
app.add_exception_handler(InvalidAmountError, invalid_amount_handler)
app.add_exception_handler(InvalidWalletIdError, invalid_wallet_id_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(WalletError, wallet_error_handler)

@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html(_credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """
    Serve custom Swagger UI documentation with authentication.

    Returns:
        HTMLResponse: Swagger UI interface
    """
    return get_swagger_ui_html(
        openapi_url=getattr(app, 'openapi_url', '/openapi.json'),
        title=getattr(app, 'title', 'FastAPI') + ' - Swagger UI',
        oauth2_redirect_url=getattr(app, 'swagger_ui_oauth2_redirect_url', None),
        swagger_js_url='https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js',
        swagger_css_url='https://unpkg.com/swagger-ui-dist@5/swagger-ui.css',
    )

@app.get('/redoc', include_in_schema=False)
async def custom_redoc_html(_credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """
    Serve custom ReDoc documentation with authentication.

    Returns:
        HTMLResponse: ReDoc interface
    """
    return get_redoc_html(
        openapi_url=getattr(app, 'openapi_url', '/openapi.json'),
        title=getattr(app, 'title', 'FastAPI') + ' - ReDoc',
        redoc_js_url='https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js',
    )

@app.get('/ping')
async def ping():
    """
    Health check endpoint to verify API is running.

    Returns:
        dict: Simple health status response
    """
    return {'message': 'pong', 'status': 'ok'}
