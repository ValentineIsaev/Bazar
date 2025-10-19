from abc import abstractmethod
from typing import Any
import math

from bot.configs.constants import ROW_BUTTON_CATALOG_MENU

from bot.services.product.services import CatalogMenuService
from bot.services.product.dto import Product

from bot.utils.message_utils.message_utils import create_list_message
from bot.utils.message_utils.message_setting_classes import MessageSetting
from bot.utils.message_utils.keyboard_utils import (create_callback_inline_keyboard,
                                                    add_callback_inline_keyboard,
                                                    generate_number_buttons,
                                                    parse_callback, InlineButtonSetting)

from .templates.messages import *
from .templates.keyboard import CATALOG_MENU_NEXT, CATALOG_MENU_BACK, PRODUCT_ACTIONS

from bot.utils.message_utils.message_setting_classes import CallbackSetting


class CatalogRenderer:
    def __init__(self, callback_prefix: CallbackSetting):
        self._prefix = callback_prefix

    @abstractmethod
    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        pass

    def _generate_list_catalog(self, page_data: tuple[tuple[int, Any], ...]):
        result = ''
        lines = math.ceil(len(page_data) / 2)

        for i in range(lines):
            for j in range(2):
                index = i + j * lines
                if index < len(page_data):
                    result += f'{str(page_data[index][1])}{5*"\t"}'
            result += '\n'

        return result

    def _generate_buttons(self, page_data: tuple[tuple[int, Any], ...]) -> tuple[InlineButtonSetting, ...]:
        return tuple(InlineButtonSetting(text=str(i+1),
                                         callback=f'{self._prefix.callback}-{j[0]}') for i, j in enumerate(page_data))


    def get_id_by_callback(self, callback: str) -> int:
        return int(callback.replace(f'{self._prefix}-', ''))

    def render_message(self, catalog_service: CatalogMenuService) -> MessageSetting:
        message = self._render_main_body(catalog_service)

        if message.text is None:
            message.text = ''
        message.text = HEADER_CATALOG_TEXT + message.text

        additional_keyboard = ((CATALOG_MENU_BACK if not catalog_service.is_start_page else ()) +
                               (CATALOG_MENU_NEXT if not catalog_service.is_end_page else ()))
        keyboard = message.keyboard
        message.keyboard = create_callback_inline_keyboard(*additional_keyboard, row=2) if keyboard is None \
            else add_callback_inline_keyboard(keyboard, *additional_keyboard, row=2)

        return message


class CategoryCatalogRenderer(CatalogRenderer):
    def __init__(self, callback_prefix: CallbackSetting):
        super().__init__(callback_prefix)

    def _render_main_body(self, catalog_service) -> MessageSetting:
        page_catalogs = catalog_service.get_page_catalogs()
        text = self._generate_list_catalog(page_catalogs) + HEADER_CATALOG_MENU_TEXT
        keyboard = create_callback_inline_keyboard(*self._generate_buttons(page_catalogs),
                                                   row=ROW_BUTTON_CATALOG_MENU)

        return MessageSetting(text=text, keyboard=keyboard)

# class ProductCatalogHierarchyManager(CatalogManager):
#     def __init__(self, catalog_service: CatalogMenuService, choice_callback: str):
#         super().__init__(catalog_service)
#
#         self._choice_callback = choice_callback
#
#     @property
#     def choice_callback(self):
#         return self._choice_callback
#
#     def _render_message(self) -> MessageSetting:
#         catalog_data = self._catalog_servie.get_catalogs()
#         main_text = create_list_message(catalog_data, 2) + HEADER_CATALOG_MENU_TEXT
#         keyboard = create_callback_inline_keyboard(*generate_number_buttons(0, len(catalog_data),
#                                                                             *parse_callback(self._choice_callback)),
#                                                    row=ROW_BUTTON_CATALOG_MENU)
#
#         return MessageSetting(text=main_text, keyboard=keyboard)


# class ProductCatalogManager(CatalogManager):
#     def __init__(self, catalog_service: CatalogMenuService):
#         super().__init__(catalog_service)
#
#     def _render_message(self) -> MessageSetting:
#         catalog_data = self._catalog_servie.get_catalogs()
#         if len(catalog_data) > 1:
#             raise ValueError(f'Max product on page - 2. Your: {len(catalog_data)}')
#         product: Product = catalog_data[0]
#
#         text = PRODUCT_INFO_TEXT.insert((product.catalog, product.name, product.price, product.description))
#
#         return MessageSetting(text=text, media=product.media, keyboard=PRODUCT_ACTIONS())
