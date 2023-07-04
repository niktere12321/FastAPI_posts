from pathlib import Path

from pydantic import BaseSettings
from pydantic.tools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR.joinpath(".env")


class Settings(BaseSettings):
    """Настройки проекта."""
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    SECRET: str = 'SECRET'

    @property
    def database_url(self):
        """Получить ссылку для подключения к DB."""
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ENV_FILE


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
