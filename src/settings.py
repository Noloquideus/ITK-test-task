from functools import lru_cache
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv(find_dotenv('.env'))


class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    DOCS_USERNAME: str
    DOCS_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        """Get database URL"""
        return f'postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'

    @property
    def EXCLUDED_PATHS(self) -> list[str]:
        """Get excluded paths"""
        return ['/docs', '/redoc', '/openapi.json', '/health']


    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', enable_decoding=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

settings = get_settings()
