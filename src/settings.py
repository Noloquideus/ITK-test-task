from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv(find_dotenv('.env'))


class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    KEYDB_PORT: int
    KEYDB_HOST: str

    DOCS_USERNAME: str
    DOCS_PASSWORD: str

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'

    @property
    def KEYDB_URL(self):
        return f'redis://{self.KEYDB_HOST}:{self.KEYDB_PORT}'

    @property
    def EXCLUDED_PATHS(self):
        return ['/metrics']

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', enable_decoding=True)

settings = Settings()
