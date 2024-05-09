import uvicorn
import sentry_sdk
from fastapi import FastAPI
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.types import Message

from src.api.endpoints.router import ROUTER
from src.core.conf import get_settings
from src.core.settings.base import get_ssm_param


SENTRY_DSN_SSM_PARAM = get_settings().SENTRY_DSN_SSM_PARAM
if SENTRY_DSN_SSM_PARAM:
    sentry_sdk.init(
        dsn=get_ssm_param(ssm_param_name=SENTRY_DSN_SSM_PARAM),
        traces_sample_rate=0.1,
        environment=get_settings().AWS_ENVIRONMENT,
    )


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app)

    async def set_body(self, request: Request, body: bytes):
        async def receive() -> Message:
            return {'type': 'http.request', 'body': body}

        request._receive = receive

    async def get_body(self, request: Request) -> bytes:
        body = await request.body()
        await self.set_body(request, body)
        return body

    async def dispatch(self, request: Request, call_next):
        await self.set_body(request, await request.body())

        body = await self.get_body(request)

        try:
            response = await call_next(request)
        except Exception:
            logger.error(f'{request.method} {request.url._url} {body} resp code=500')
            raise
        else:
            logger.info(
                f'{request.method} {request.url._url} {body if len(body) < 1024 else ""} resp code={response.status_code}'
            )

        return response


app = FastAPI(
    **get_settings().fastapi_kwargs,
    generate_unique_id_function=lambda route: route.name,
    swagger_ui_parameters={'displayRequestDuration': True},
)
app.logger = logger
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*']
)
app.add_middleware(LoggingMiddleware)
app.include_router(ROUTER)

Instrumentator(
    excluded_handlers=['.*/docs', '.*/redoc', '.*/openapi.json', '.*/metrics'],
    should_group_status_codes=False,
    inprogress_labels=True,
).instrument(app).expose(app, endpoint='/metrics', include_in_schema=False)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
