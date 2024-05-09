from abc import abstractmethod
from typing import Any

from aws_lambda_powertools.utilities import parameters
from pydantic import BaseSettings

from sqlalchemy.engine import URL


def get_ssm_param(ssm_param_name: str, max_age: int = 60):
    """Get a secret value from AWS Systems Manager Parameter Store

    Retrieves the value of a parameter from AWS Systems Manager Parameter Store.

    Args:
    ssm_param_name: The name of the parameter in SSM Parameter Store
    max_age: The maximum acceptable age in seconds of the parameter value.

    Returns:
    The value of the parameter as a string.
    """
    return parameters.get_parameter(ssm_param_name, max_age=max_age)


class AppSettings(BaseSettings):
    service_name: str = 'user-service'
    debug: bool = False
    docs_url: str = f'/{service_name}/docs'
    openapi_prefix: str = ''
    openapi_url: str = f'/{service_name}/openapi.json'
    redoc_url: str = f'/{service_name}/redoc'
    title: str = 'Users service'
    version: str = '0.0.1'

    AWS_ENVIRONMENT: str = 'dev'
    SENTRY_DSN_SSM_PARAM: str = None

    class Config:
        allow_mutation = False

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            'debug': self.debug,
            'docs_url': self.docs_url,
            'openapi_prefix': self.openapi_prefix,
            'openapi_url': self.openapi_url,
            'redoc_url': self.redoc_url,
            'title': self.title,
            'version': self.version,
        }

    @abstractmethod
    def get_db_url(self, async_: bool = True) -> URL:
        raise NotImplementedError
