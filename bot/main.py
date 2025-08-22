from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.core.setup import setup
from database.core import SessionLocal

from handlers import (seller_router,
                      buyer_router,
                      common_router,
                      catalog_menu_router,
                      unexpected_router)

from bot.middlewares.di_middlewares import DIMiddleware, DIUserMiddleware, UserSessionMiddleware
from bot.middlewares.database_middlewares import DBSessionMiddleware

from bot.services.product.services import ProductService
from bot.managers.mediator.manager import MediatorManager
from bot.managers.session_manager.session import SessionManager

from bot.redis.core import user_session_redis

import asyncio


async def main():
    bot = setup()
    dp = Dispatcher(storage=MemoryStorage())

    product_service = ProductService()

    di_middleware = DIMiddleware(product_service=product_service)
    user_session = SessionManager(user_session_redis)
    user_session_middleware = UserSessionMiddleware(user_session)
    # di_user_middleware = DIUserMiddleware(mediator_manager=lambda: MediatorManager(user_session))
    db_session_middleware = DBSessionMiddleware(SessionLocal)

    dp.message.middleware(user_session_middleware)
    dp.message.middleware(di_middleware)
    # dp.message.middleware(di_user_middleware)
    dp.callback_query(user_session_middleware)
    dp.callback_query.middleware(di_middleware)
    # dp.callback_query.middleware(di_user_middleware)
    dp.message.middleware(db_session_middleware)
    dp.callback_query.middleware(db_session_middleware)

    dp.include_routers(common_router, seller_router, buyer_router, catalog_menu_router)
    print('Start bot!')

    dp.include_router(unexpected_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
