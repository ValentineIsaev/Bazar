from abc import abstractmethod

from aiogram.fsm.context import FSMContext

from bot.configs.constants import ROW_BUTTON_CATALOG_MENU

from bot.services.product.services import CatalogMenuService
from bot.services.product.dto import Product

from bot.utils.message_utils.media_messages_utils import delete_media_message
from bot.utils.message_utils.message_utils import create_list_message, send_message
from bot.utils.message_utils.message_setting_classes import MessageSetting
from bot.utils.message_utils.keyboard_utils import (create_callback_inline_keyboard,
                                                    add_callback_inline_keyboard,
                                                    generate_number_buttons,
                                                    parse_callback)

from .templates.messages import *
from .templates.keyboard import CATALOG_MENU_NEXT, CATALOG_MENU_BACK, PRODUCT_ACTIONS

class CatalogManager:
    SCROLL_NEXT = 'next'
    SCROLL_BACK = 'back'


    def __init__(self, catalog_service: CatalogMenuService):
        self._catalog_servie = catalog_service

    def scroll_catalog(self, mode: str):
        if mode == self.SCROLL_NEXT:
            self._catalog_servie.next_page()
        elif mode == self.SCROLL_BACK:
            self._catalog_servie.back_page()
        else:
            raise ValueError(f'Mode {mode} is wrong. Or {self.SCROLL_NEXT}, or {self.SCROLL_BACK}')

    @property
    def catalog(self):
        return self._catalog_servie.get_catalogs()

    @abstractmethod
    def _render_message(self) -> MessageSetting:
        pass

    def create_message(self) -> MessageSetting:
        message = self._render_message()

        if message.text is None:
            message.text = ''
        message.text = HEADER_CATALOG_TEXT + message.text

        additional_keyboard = ((CATALOG_MENU_BACK if not self._catalog_servie.is_start_page else ()) +
                               (CATALOG_MENU_NEXT if not self._catalog_servie.is_end_page else ()))
        keyboard = message.keyboard
        message.keyboard = create_callback_inline_keyboard(*additional_keyboard, row=2) if keyboard is None \
            else add_callback_inline_keyboard(keyboard, *additional_keyboard, row=2)

        return message


class ProductCatalogHierarchyManager(CatalogManager):
    def __init__(self, catalog_service: CatalogMenuService, choice_callback: str):
        super().__init__(catalog_service)

        self._choice_callback = choice_callback

    @property
    def choice_callback(self):
        return self._choice_callback

    def _render_message(self) -> MessageSetting:
        catalog_data = self._catalog_servie.get_catalogs()
        main_text = create_list_message(catalog_data, 2) + HEADER_CATALOG_MENU_TEXT
        keyboard = create_callback_inline_keyboard(*generate_number_buttons(0, len(catalog_data),
                                                                            *parse_callback(self._choice_callback)),
                                                   row=ROW_BUTTON_CATALOG_MENU)

        return MessageSetting(text=main_text, keyboard=keyboard)


class ProductCatalogManager(CatalogManager):
    def __init__(self, catalog_service: CatalogMenuService):
        super().__init__(catalog_service)

    def _render_message(self) -> MessageSetting:
        catalog_data = self._catalog_servie.get_catalogs()
        if len(catalog_data) > 1:
            raise ValueError(f'Max product on page - 2. Your: {len(catalog_data)}')
        product: Product = catalog_data[0]

        text = PRODUCT_INFO_TEXT.insert((product.catalog, product.name, product.price, product.description))

        return MessageSetting(text=text, media=product.media, keyboard=PRODUCT_ACTIONS())
