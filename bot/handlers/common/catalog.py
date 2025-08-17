from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery

from bot.configs.constants import ParamFSM
from bot.services.product.models import CatalogMenu
from bot.utils.message_utils.message_setting_classes import MessageSetting
from bot.utils.message_utils.keyboard_utils import (parse_callback)
from bot.utils.filters import CallbackFilter
from bot.utils.catalog_utils.catalog_utils import create_catalog_message, send_catalog_message

catalog_menu_router = Router()


@catalog_menu_router.callback_query(CallbackFilter('catalog_menu'))
async def scroll_catalog_menu(cb: CallbackQuery, state: FSMContext):
    _, subscope, action = parse_callback(cb.data)

    if subscope == 'scroll':
        user_data = await state.get_data()
        catalog_menu: CatalogMenu = user_data.get(ParamFSM.BotMessagesData.CatalogData.CATALOG_MENU)

        if action == 'next':
            catalog_menu.next_page()
        elif action == 'back':
            catalog_menu.back_page()

        new_msg: MessageSetting = await create_catalog_message(state)
        await send_catalog_message(state, cb.bot, new_msg)
