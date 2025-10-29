from pathlib import Path
import shutil

from bot.dependencies import (DIMiddleware, set_product_manager, set_input_product_manager, set_catalog_manager,
                              set_product_category_catalog_manager, set_media_consolidator)

from bot.storage.postgres import SessionLocal
from bot.storage.redis.core import user_session_redis

from bot.configs.configs import bot_configs

from aiogram import Bot, Dispatcher

async def set_dependencies(dp: Dispatcher):
    async with SessionLocal() as session:
        dp['db_session'] = session

    di_middleware = DIMiddleware(product_manager=set_product_manager,
                                 input_product_manager=set_input_product_manager,
                                 catalog_manager=set_catalog_manager,
                                 product_category_catalog_manager=set_product_category_catalog_manager,
                                 media_consolidator=set_media_consolidator)
    dp.message.middleware(di_middleware)
    dp.callback_query.middleware(di_middleware)

def clear_cache(cache_dir: Path):
    for d in cache_dir.rglob('*'):
        print(d, d.parent)
        if d.is_dir() and d.parent != cache_dir:
            shutil.rmtree(d)


async def setup() -> Bot:
    # clear_cache(cache_configs.CACHE_DIR)
    bot = Bot(bot_configs.BOT_TOKEN.get_secret_value())

    await user_session_redis.flushdb()

    return bot
