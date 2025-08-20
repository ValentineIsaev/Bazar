from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.core.setup import setup

from handlers import (seller_router,
                      buyer_router,
                      common_router,
                      catalog_menu_router,
                      unexpected_router)

from bot.dependencies.middlewares import DIProductServiceMiddleware
from bot.services.product.services import ProductService

import asyncio


async def main():
    bot = setup()
    dp = Dispatcher(storage=MemoryStorage())

    product_service = ProductService()
    dp.message.middleware(DIProductServiceMiddleware(product_service))
    dp.callback_query.middleware(DIProductServiceMiddleware(product_service))

    dp.include_routers(common_router, seller_router, buyer_router, catalog_menu_router)
    print(id(seller_router))

    dp.include_router(unexpected_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
