from fastapi import Depends, status

from praktika_shared_lib.fastapi.router import SchemaRouter
from praktika_shared_lib.fastapi.http_exceptions import BadRequestException

from src.core.conf import get_settings
from src.api.crud.user import UserCRUD
from src.api.dependencies.auth import validate_user_id, get_current_user
from src.api.dependencies.transaction import Transaction
from src.api.endpoints.schemas.user import (
    UserOutputModel,
    UserUpdateModel,
    UserCreateModel,
)
from src.api.models.user import User


router = SchemaRouter()
settings = get_settings()


@router.get('/{user_id}', response_model=UserOutputModel)
async def get_user(user: User = Depends(get_current_user)):
    return UserOutputModel(**user.dict())


@router.patch('/{user_id}', response_model=UserOutputModel)
async def update_user(
    user_update: UserUpdateModel, user_id: str = Depends(validate_user_id), transaction: Transaction = Depends()
):
    async with transaction:
        user = await UserCRUD.get_or_create_user(transaction.db_session, user_id)

        user = await UserCRUD.update_user(transaction.db_session, user, user_update)
        return UserOutputModel(**user.dict())


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel, transaction: Transaction = Depends()):
    if user_data.id is not None:
        session = transaction.db_session
        if await UserCRUD.get_user(session, user_data.id) is not None:
            raise BadRequestException(detail=f"User with ID {user_data.id} already exists")
    async with transaction:
        user = await UserCRUD.create_user(transaction.db_session, user_data)
        return UserOutputModel(**user.dict())


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: User = Depends(get_current_user), transaction: Transaction = Depends()):
    async with transaction:
        await UserCRUD.delete_user(transaction.db_session, user)
