from uuid import UUID

from praktika_shared_lib.db import MyAsyncSession

from src.api.endpoints.schemas.user import UserCreateModel, UserUpdateModel
from src.api.models.user import User


class UserCRUD:
    @classmethod
    async def get_user(cls, db_session: MyAsyncSession, user_id: UUID | str) -> User | None:
        return await db_session.get(User, user_id)

    @classmethod
    async def create_user(cls, db_session: MyAsyncSession, user_data: UserCreateModel) -> User:
        create_data = user_data.dict(exclude_unset=True)
        new_user = User(**create_data)
        db_session.add(new_user)
        await db_session.flush()
        return await db_session.get(User, new_user.id)

    @classmethod
    async def get_or_create_user(cls, db_session: MyAsyncSession, user_id: UUID | str) -> User:
        user = await cls.get_user(db_session, user_id)
        if user is None:
            user = await cls.create_user(db_session, UserCreateModel(id=user_id))
        return user

    @classmethod
    async def update_user(cls, db_session: MyAsyncSession, user: User, user_data: UserUpdateModel) -> User:
        update_data = user_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        db_session.add(user)
        await db_session.flush([user])
        return user

    @classmethod
    async def delete_user(cls, db_session: MyAsyncSession, user: User) -> None:
        await db_session.delete(user)
        await db_session.flush([user])
