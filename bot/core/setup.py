from pathlib import Path
import shutil

from bot.dependencies import (DIMiddleware, InputMediaMiddleWare,set_product_manager, set_input_product_manager, set_catalog_manager,
                              set_product_category_catalog_manager, SetterMediaConsolidator, set_mediator_manager)

from bot.storage.postgres import SessionLocal
from bot.storage.redis.core import user_session_redis

from bot.configs.configs import bot_configs, media_storage_data

from aiogram import Bot, Dispatcher

async def set_dependencies(dp: Dispatcher, bot: Bot):
    async with SessionLocal() as session:
        dp['db_session'] = session

    set_media_consolidator = SetterMediaConsolidator(bot, media_storage_data.TEMP_STORAGE_PATH,
                                                     media_storage_data.PERM_STORAGE_PATH)
    media_middleware = InputMediaMiddleWare(set_media_consolidator())

    di_middleware = DIMiddleware(product_manager=set_product_manager,
                                 input_product_manager=set_input_product_manager,
                                 catalog_manager=set_catalog_manager,
                                 products_catalog_manager=set_product_category_catalog_manager,
                                 media_consolidator=set_media_consolidator,
                                 mediator_manager=set_mediator_manager,
                                 media_middleware=lambda _: media_middleware)

    dp.message.middleware(di_middleware)
    dp.message.middleware(media_middleware)
    dp.callback_query.middleware(di_middleware)
    dp.callback_query.middleware(media_middleware)


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
