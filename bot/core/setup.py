from pathlib import Path
import shutil

from bot.dependencies import DIMiddleware, get_product_manager

from bot.storage.database import SessionLocal
from bot.storage.redis.core import user_session_redis

from bot.configs.configs import cache_configs, bot_configs

from aiogram import Bot, Dispatcher

async def set_dependencies(dp: Dispatcher):
    async with SessionLocal() as session:
        dp['db_session'] = session

    di_middleware = DIMiddleware(product_manager=get_product_manager)
    dp.message.middleware(di_middleware)
    dp.callback_query.middleware(di_middleware)

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
