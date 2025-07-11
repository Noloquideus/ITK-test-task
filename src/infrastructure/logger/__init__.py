from src.infrastructure.logger.log_format import LogFormat
from src.infrastructure.logger.log_levels import LogLevel
from src.infrastructure.logger.logger import Logger


logger = Logger(min_level=LogLevel.DEBUG, log_format=LogFormat.JSON)


async def get_logger() -> Logger:
    return logger
