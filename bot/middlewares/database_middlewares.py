from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker

class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory

    async def __call__(self, handler, event, data):
        async with self._session_factory() as session:
            data['db_session'] = session
            return await handler(event, data)