from abc import ABC, abstractmethod

from aiogram.fsm.context import FSMContext

from .messages import HEADER_CATALOG_MENU_TEXT

from bot.handlers.buyer.templates.keyboard import PRODUCT_ACTIONS
from bot.handlers.buyer.templates.messages import PRODUCT_INFO_TEXT

from bot.services.product.dto import Product

from bot.utils.helper import get_data_state
from bot.utils.message_utils.message_setting_classes import MessageSetting
from bot.utils.message_utils.message_utils import create_list_message
from bot.utils.message_utils.keyboard_utils import (parse_callback, generate_number_buttons,
                                                    create_callback_inline_keyboard)

from bot.configs.constants import ROW_BUTTON_CATALOG_MENU, ParamFSM


class CatalogRender(ABC):
    @abstractmethod
    async def rendering_data(self, state: FSMContext, catalog_data: tuple) -> MessageSetting:
        pass


class MenuCatalogRender(CatalogRender):
    async def rendering_data(self, state: FSMContext, catalog_data: tuple) -> MessageSetting:
        (callback_setting,) = await get_data_state(state,
                                                ParamFSM.BotMessagesData.CatalogData.CATALOG_MENU_CALLBACK)

        main_text = create_list_message(catalog_data,2) + HEADER_CATALOG_MENU_TEXT
        keyboard = create_callback_inline_keyboard(*generate_number_buttons(0, len(catalog_data),
                                                *parse_callback(callback_setting)),row=ROW_BUTTON_CATALOG_MENU)

        return MessageSetting(text=main_text, keyboard=keyboard)


class ProductCatalogRender(CatalogRender):
    async def rendering_data(self, state: FSMContext, catalog_data: tuple) -> MessageSetting:
        if len(catalog_data) > 1:
            raise ValueError(f'Max product on page - 2. Your: {len(catalog_data)}')
        product: Product = catalog_data[0]

        text = PRODUCT_INFO_TEXT.insert((product.catalog, product.name, product.price, product.description))

        return MessageSetting(text=text, media=product.media, keyboard=PRODUCT_ACTIONS())
