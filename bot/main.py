from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.core.setup import setup, registration_middlewares

from handlers import (seller_router,
                      buyer_router,
                      common_router,
                      catalog_menu_router,
                      unexpected_router)

from bot.services.product.services import ProductService

import asyncio


async def main():
    bot = await setup()
    dp = Dispatcher(storage=MemoryStorage())

    registration_middlewares(dp)

    dp.include_routers(common_router, seller_router, buyer_router, catalog_menu_router)
    print('Start bot!')

    dp.include_router(unexpected_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
