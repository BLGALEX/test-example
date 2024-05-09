from praktika_shared_lib.db import MyAsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.conf import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.get_db_url(), echo=settings.debug, pool_size=50, max_overflow=50, pool_recycle=3600
)


LocalSession = sessionmaker(engine, class_=MyAsyncSession, expire_on_commit=False)


async def get_db() -> MyAsyncSession:
    async with LocalSession() as session:
        yield session
