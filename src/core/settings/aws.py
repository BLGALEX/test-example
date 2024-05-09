import json
import os

import boto3
from sqlalchemy.engine import URL

from src.core.settings.base import AppSettings


class AwsSettings(AppSettings):
    DB_DATABASE: str

    def get_db_url(self, async_: bool = True) -> URL:
        client = boto3.client('secretsmanager', region_name='us-east-1')
        db_secret_arn = os.environ['DB_SECRET_ARN']
        secret_value = json.loads(client.get_secret_value(SecretId=db_secret_arn)['SecretString'])
        db_host = os.getenv('DB_HOST', secret_value['host'])
        return URL.create(
            'postgresql+asyncpg' if async_ else 'postgresql',
            secret_value['username'],
            secret_value['password'] or None,
            db_host,
            secret_value['port'],
            self.DB_DATABASE,
        )
