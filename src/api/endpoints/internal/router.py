from fastapi import APIRouter

from src.api.endpoints.internal import user

INTERNAL_ROUTER = APIRouter(tags=['internal'])

INTERNAL_ROUTER.include_router(user.router, prefix='/users')
