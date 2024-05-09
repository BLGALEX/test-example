from fastapi import APIRouter

from praktika_shared_lib.fastapi.endpoints.health import health_router

from src.api.endpoints.internal import router as internal_router
from src.core.conf import get_settings

settings = get_settings()


ROUTER = APIRouter(prefix=f"/{settings.service_name}")
ROUTER.include_router(health_router)
ROUTER.include_router(internal_router.INTERNAL_ROUTER)
