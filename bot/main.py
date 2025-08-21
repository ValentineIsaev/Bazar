from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.core.setup import setup

from handlers import (seller_router,
                      buyer_router,
                      common_router,
                      catalog_menu_router,
                      unexpected_router)

from bot.middlewares.di_middlewares import DIMiddleware
from bot.services.product.services import ProductService

import asyncio


async def main():
    bot = setup()
    dp = Dispatcher(storage=MemoryStorage())

    product_service = ProductService()
    di_middleware = DIMiddleware(product_service=product_service)
    dp.message.middleware(di_middleware)
    dp.callback_query.middleware(di_middleware)

    dp.include_routers(common_router, seller_router, buyer_router, catalog_menu_router)
    print('Start bot!')

    dp.include_router(unexpected_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
