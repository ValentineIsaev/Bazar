from abc import ABC, abstractmethod

from aiogram.fsm.context import FSMContext

from bot.services.product.models import Product

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

        main_text = create_list_message(catalog_data,2)
        keyboard = create_callback_inline_keyboard(*generate_number_buttons(0, len(catalog_data),
                                                *parse_callback(callback_setting)),row=ROW_BUTTON_CATALOG_MENU)

        return MessageSetting(text=main_text, keyboard=keyboard)


class ProductCatalogRender(CatalogRender):
    async def rendering_data(self, state: FSMContext, catalog_data: tuple) -> MessageSetting:
        product: Product = catalog_data[0]
        return MessageSetting(text=product.name, media=product.media)
