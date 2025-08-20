from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery

from bot.configs.constants import ParamFSM
from bot.services.product.services import CatalogMenuService
from bot.utils.message_utils.message_setting_classes import MessageSetting
from bot.utils.message_utils.keyboard_utils import (parse_callback)
from bot.utils.filters import CallbackFilter
from bot.managers.catalog_manager.catalog_managers import CatalogManager
from bot.utils.helper import get_data_state
from bot.utils.message_utils.message_utils import send_message

catalog_menu_router = Router()


@catalog_menu_router.callback_query(CallbackFilter('catalog_menu'))
async def scroll_catalog_menu(cb: CallbackQuery, state: FSMContext):
    _, subscope, action = parse_callback(cb.data)

    catalog_manager: CatalogManager
    (catalog_manager,) = await get_data_state(state, ParamFSM.BotMessagesData.CATALOG_MANAGER)
    if subscope == 'scroll':
        catalog_manager.scroll_catalog(action)
        await state.update_data(**{ParamFSM.BotMessagesData.CATALOG_MANAGER: catalog_manager})
        new_msg: MessageSetting = catalog_manager.create_message()
        await send_message(state, cb.bot, new_msg)
