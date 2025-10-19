from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery

from bot.storage.redis import FSMStorage
from bot.utils.message_utils.message_utils import send_message
from bot.utils.message_utils.keyboard_utils import (parse_callback)
from bot.utils.filters import CallbackFilter
from bot.managers.catalog_manager import CatalogManager

catalog_menu_router = Router()


@catalog_menu_router.callback_query(CallbackFilter('catalog_menu'))
async def scroll_catalog_menu(cb: CallbackQuery, fsm_storage: FSMStorage, catalog_manager: CatalogManager):
    _, subscope, action = parse_callback(cb.data)

    if subscope == 'scroll':
        await catalog_manager.scroll_catalog(action)
        await send_message(fsm_storage, cb.bot, await catalog_manager.render_message(), False)
