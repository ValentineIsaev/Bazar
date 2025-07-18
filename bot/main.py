from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import seller_router, buyer_router, common_router, catalog_menu_router, unexpected_router
from configs.configs import TOKEN

import asyncio


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(common_router, seller_router, buyer_router, catalog_menu_router)
    print(id(seller_router))

    dp.include_router(unexpected_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
