import os
import pathlib
import subprocess
import sys

from loguru import logger

from src.core.conf import get_settings

CURRENT_PATH = pathlib.Path(__file__).parent.resolve()


def run_migrations():
    db_url = get_settings().get_db_url(async_=False)

    if os.environ['ENVIRONMENT'] in ['local', 'test']:
        require_ssl = False
    else:
        require_ssl = True

    DATABASE_URL = f'{db_url}?sslmode={"require" if require_ssl else "disable"}'

    dbmate_binary_name = 'dbmate-macos-amd64' if sys.platform.lower() == 'darwin' else 'dbmate-linux-amd64'

    logger.info('Running DB migrations')
    subprocess.check_output(
        f'DATABASE_URL={DATABASE_URL} {CURRENT_PATH}/dbmate_bin/{dbmate_binary_name} -d {CURRENT_PATH}/migrations up',
        stderr=subprocess.STDOUT,
        shell=True,
    )
    logger.info('DB migrations finished successfully')


if __name__ == '__main__':
    run_migrations()
