from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery

from bot.configs.constants import ParamFSM, ROW_BUTTON_CATALOG_MENU
from bot.services.product.models import CatalogMenu
from bot.utils.message_utils.message_utils import create_list_message, MessageSetting, send_message
from bot.utils.message_utils.keyboard_utils import (generate_number_buttons, create_callback_inline_keyboard, parse_callback,
                                                    add_callback_inline_keyboard)
from bot.utils.filters import CallbackFilter

from .keyboard import CATALOG_MENU_NEXT, CATALOG_MENU_BACK
from .messages import HEADER_CATALOG_MENU_TEXT

catalog_menu_router = Router()

async def create_catalog_message(state: FSMContext) -> MessageSetting:
    user_data = await state.get_data()

    catalog_menu: CatalogMenu = user_data.get(ParamFSM.ProductData.CATALOG_MENU)
    catalog = catalog_menu.get_catalogs()
    text = HEADER_CATALOG_MENU_TEXT + create_list_message(catalog, 2)

    callback_setting = user_data.get(ParamFSM.ProductData.CATALOG_MENU_CALLBACK)
    keyboard = create_callback_inline_keyboard(*generate_number_buttons(0, len(catalog),
                                                *parse_callback(callback_setting)),row=ROW_BUTTON_CATALOG_MENU)

    additional_keyboard = ((CATALOG_MENU_BACK if not catalog_menu.is_start_page else ()) +
                           (CATALOG_MENU_NEXT if not catalog_menu.is_end_page else ()))
    if additional_keyboard:
        keyboard = add_callback_inline_keyboard(keyboard, *additional_keyboard, row=2)

    return MessageSetting(text=text, keyboard=keyboard)


@catalog_menu_router.callback_query(CallbackFilter('catalog_menu'))
async def scroll_catalog_menu(cb: CallbackQuery, state: FSMContext):
    _, subscope, action = parse_callback(cb.data)

    if subscope == 'scroll':
        user_data = await state.get_data()
        catalog_menu: CatalogMenu = user_data.get(ParamFSM.ProductData.CATALOG_MENU)

        if action == 'next':
            catalog_menu.next_page()
        elif action == 'back':
            catalog_menu.back_page()

        await send_message(state, cb.bot, await create_catalog_message(state), False)