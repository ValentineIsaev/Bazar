from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.core.setup import setup, set_dependencies

from handlers import (seller_router,
                      buyer_router,
                      common_router,
                      catalog_menu_router,
                      mediator_router)

import asyncio


async def main():
    bot = await setup()
    dp = Dispatcher(storage=MemoryStorage())

    await set_dependencies(dp, bot)

    dp.include_routers(seller_router, buyer_router, catalog_menu_router, mediator_router, common_router)
    print('Start bot!')

    await dp.start_polling(bot, polling_timeout=60)


if __name__ == '__main__':
    asyncio.run(main())
