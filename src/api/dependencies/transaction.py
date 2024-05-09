from fastapi import Depends
from praktika_shared_lib.db import MyAsyncSession

from src.api.session import get_db


class Transaction:
    def __init__(self, db_session: MyAsyncSession = Depends(get_db)):
        self.db_session = db_session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # rollback and let the exception propagate
            await self.db_session.rollback()
            return False

        await self.db_session.commit()
        return True
