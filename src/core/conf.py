import os
from functools import lru_cache

from loguru import logger

from src.core.settings.aws import AwsSettings
from src.core.settings.base import AppSettings
from src.core.settings.local import LocalSettings
from src.core.settings.test import TestSettings

env_settings = {'local': LocalSettings, 'aws': AwsSettings, 'test': TestSettings}


@lru_cache
def get_settings() -> AppSettings:
    environment = os.environ.get('ENVIRONMENT', 'local')
    logger.info(f'Assuming {environment} environment for configuration')
    return env_settings[environment]()
