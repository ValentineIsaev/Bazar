from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.core.setup import setup

from handlers import (seller_router,
                      buyer_router,
                      common_router,
                      catalog_menu_router,
                      unexpected_router)

from bot.dependencies.dependencies import get_product_service, ProductService

import asyncio


async def main():
    bot = setup()
    dp = Dispatcher(storage=MemoryStorage())
    dp['product_service'] = get_product_service

    dp.include_routers(common_router, seller_router, buyer_router, catalog_menu_router)
    print(id(seller_router))

    dp.include_router(unexpected_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
