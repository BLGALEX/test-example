import asyncio
import os
import pytest as pytest
from httpx import AsyncClient

from sqlalchemy import delete

from praktika_shared_lib.db import Base

from db.run_migrations import run_migrations
from src.app import app as app_
from src.api.session import LocalSession
from .factories import UserModelFactory

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture
async def app():
    return app_


@pytest.fixture(autouse=True)
async def truncate_db():
    yield
    async with LocalSession.begin() as db:
        for table in reversed(Base.metadata.sorted_tables):
            await db.execute(delete(table))


@pytest.fixture(scope='session', autouse=True)
def migrate_database():
    run_migrations()
    yield


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url='http://test/user-service/users') as client_:
        yield client_


@pytest.fixture
def create_user():
    async def _create_user(**kwargs):
        user = UserModelFactory(**kwargs)
        async with LocalSession.begin() as db:
            db.add(user)
        return user

    return _create_user
