from sqlalchemy.engine import URL

from src.core.settings.base import AppSettings
from src.core.settings.local import LocalSettings


class TestSettings(LocalSettings):
    debug: bool = False

    class Config(AppSettings.Config):
        env_file = 'env/test-local.env'

    def get_db_url(self, async_: bool = True) -> URL:
        return URL.create(
            'postgresql+asyncpg' if async_ else 'postgresql',
            self.DB_USER,
            self.DB_PASSWORD.get_secret_value() or None,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_DATABASE,
        )
