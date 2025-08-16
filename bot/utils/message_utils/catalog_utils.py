from aiogram.fsm.context import FSMContext

from .message_setting_classes import MessageSetting
from .message_utils import create_list_message
from .keyboard_utils import (create_callback_inline_keyboard, generate_number_buttons, parse_callback,
                             add_callback_inline_keyboard, InlineButtonSetting, create_callback)
from ..helper import get_data_state

from bot.services.product.models import CatalogMenu
from bot.configs.constants import ParamFSM, ROW_BUTTON_CATALOG_MENU

HEADER_CATALOG_MENU_TEXT = ('Используйте кнопки для выбора номера нужного каталога, '
                            'а также кнопки вперед и назад для пролистывания.\n\n')

CATALOG_MENU_NEXT = (InlineButtonSetting(text='Вперед', callback=create_callback('catalog_menu',
                                                                                'scroll',
                                                                                'next')),)
CATALOG_MENU_BACK = (InlineButtonSetting(text='Назад', callback=create_callback('catalog_menu',
                                                                                'scroll',
                                                                                'back')),)


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

async def repack_choice_catalog_data(callback: str, state: FSMContext):
    catalog_menu: CatalogMenu
    catalog_menu, catalog_callback  = await get_data_state(state, ParamFSM.ProductData.CATALOG_MENU,
                                           ParamFSM.ProductData.CATALOG_MENU_CALLBACK)

    number_catalog = int(callback.replace(f'{catalog_callback}-', ''))

    selected_catalog = catalog_menu.get_catalogs()[number_catalog]
    return selected_catalog

async def create_catalog(state: FSMContext, choice_callback: str, catalog_menu: CatalogMenu) -> MessageSetting:
    await state.update_data(**{ParamFSM.ProductData.CATALOG_MENU: catalog_menu,
                               ParamFSM.ProductData.CATALOG_MENU_CALLBACK: choice_callback})

    return await create_catalog_message(state)