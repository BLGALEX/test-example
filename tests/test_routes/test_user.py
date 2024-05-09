import pytest
import uuid

from sqlalchemy import select

from src.api.models.user import User
from src.api.session import LocalSession

from tests.factories import UserModelFactory


pytestmark = pytest.mark.asyncio


async def test_get_user(client, create_user):
    user = await create_user()

    response = await client.get(f"/{user.id}")

    assert response.status_code == 200, response.text
    assert str(user.id) == response.json()["id"]


async def test_get_user_not_found(client):
    response = await client.get(f"/{uuid.uuid4()}")

    assert response.status_code == 404, response.text


async def test_post_user(client):
    user = UserModelFactory.build()

    response = await client.post("/", json={"id": str(user.id)})

    assert response.status_code == 201, response.text
    query = select(User).filter(User.id == user.id)
    async with LocalSession.begin() as db:
        assert (await db.execute(query)).scalar_one()


async def test_post_user_id_already_exists(client, create_user):
    user = await create_user()

    response = await client.post("/", json={"id": str(user.id)})

    assert response.status_code == 400, response.text
    assert "already exists" in response.json()["detail"].lower()


async def test_patch_user(client, create_user):
    user = await create_user()
    new_user = UserModelFactory.build()

    response = await client.patch(f"/{user.id}", json=new_user.dict())

    assert response.status_code == 200, response.text
    query = select(User).filter(User.id == user.id)
    async with LocalSession.begin() as db:
        updated_user = (await db.execute(query)).scalar_one()
    assert str(updated_user.id) == user.id
    assert updated_user.name == new_user.name
    assert updated_user.email == new_user.email


async def test_patch_user_create_if_not_found(client):
    new_user = UserModelFactory.build()

    response = await client.patch(f"/{uuid.uuid4()}", json=new_user.dict())

    assert response.status_code == 200, response.text
    query = select(User).filter(User.email == new_user.email)
    async with LocalSession.begin() as db:
        updated_user = (await db.execute(query)).scalar_one()
    assert updated_user.email == new_user.email


async def test_delete_user(client, create_user):
    user = await create_user()

    response = await client.delete(f"/{user.id}")

    assert response.status_code == 204, response.text
    assert response.text == ""
    query = select(User).filter(User.id == user.id)
    async with LocalSession.begin() as db:
        assert (await db.execute(query)).scalar_one_or_none() is None


async def test_delete_user_not_found(client):
    response = await client.delete(f"/{uuid.uuid4()}")

    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "User not found"
