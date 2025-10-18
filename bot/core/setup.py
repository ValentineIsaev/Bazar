from pathlib import Path
import shutil

from bot.middlewares.di_middlewares import DIMiddleware, UserSessionMiddleware, DIUserMiddleware
from bot.middlewares.database_middlewares import DBSessionMiddleware

from bot.managers.session_manager.session import SessionManager
from bot.services.product.services import ProductService
from bot.storage.database.core import SessionLocal
from bot.managers.mediator.manager import MediatorManager

from bot.storage.redis.core import user_session_redis

from bot.configs.configs import cache_configs, bot_configs

from aiogram import Bot, Dispatcher

user_session_manager = SessionManager(user_session_redis)
product_service = ProductService()

di_middleware = DIMiddleware(product_service=product_service)
user_session_middleware = UserSessionMiddleware(user_session_manager)
db_session_middleware = DBSessionMiddleware(SessionLocal)
di_user_middleware = DIUserMiddleware(mediator_manager=lambda: MediatorManager(user_session_manager))

def registration_middlewares(dp: Dispatcher):
    dp.message.middleware(di_middleware)
    dp.message.middleware(di_user_middleware)
    dp.message.middleware(user_session_middleware)
    dp.message.middleware(db_session_middleware)

    dp.callback_query.middleware(di_middleware)
    dp.callback_query.middleware(di_user_middleware)
    dp.callback_query.middleware(user_session_middleware)
    dp.callback_query.middleware(db_session_middleware)

def clear_cache(cache_dir: Path):
    for d in cache_dir.rglob('*'):
        print(d, d.parent)
        if d.is_dir() and d.parent != cache_dir:
            shutil.rmtree(d)


async def setup() -> Bot:
    clear_cache(cache_configs.CACHE_DIR)
    bot = Bot(bot_configs.BOT_TOKEN.get_secret_value())

    await user_session_redis.flushdb()

    return bot
