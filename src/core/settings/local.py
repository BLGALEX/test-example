import pathlib

from pydantic import SecretStr
from sqlalchemy.engine import URL

from src.core.settings.base import AppSettings

CURRENT_PATH = pathlib.Path(__file__).parent.resolve()


class LocalSettings(AppSettings):
    debug: bool = False

    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str

    class Config(AppSettings.Config):
        env_file = f'{CURRENT_PATH}/../../../env/local.env'

    def get_db_url(self, async_: bool = True) -> URL:
        return URL.create(
            'postgresql+asyncpg' if async_ else 'postgresql',
            self.DB_USER,
            self.DB_PASSWORD.get_secret_value() or None,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_DATABASE,
        )
