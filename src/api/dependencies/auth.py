from uuid import UUID

from fastapi import Depends, Path

from praktika_shared_lib.db import MyAsyncSession
from praktika_shared_lib.fastapi.http_exceptions import BadRequestException, NotFoundException

from src.api.crud.user import UserCRUD
from src.api.models.user import User
from src.api.session import get_db


def validate_user_id(user_id: UUID = Path(..., title="The User ID")) -> UUID:
    if not user_id:
        raise BadRequestException(detail="User ID header not provided")
    return user_id


async def get_current_user(user_id: UUID = Depends(validate_user_id), db: MyAsyncSession = Depends(get_db)) -> User:
    user = await UserCRUD.get_user(db, user_id)
    if not user:
        raise NotFoundException(detail="User not found")
    return user
