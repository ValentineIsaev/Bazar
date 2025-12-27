from abc import abstractmethod
from typing import Any
import math

from bot.configs.constants import ROW_BUTTON_CATALOG_MENU

from bot.services.catalog_service import CatalogMenuService
from bot.types.utils import MediaSetting

from bot.types.utils import MessageSetting, CallbackSetting
from bot.utils.message_utils.keyboard_utils import (get_callback_inline_keyboard,
                                                    InlineButtonSetting)

from .templates.messages import *
from .templates.keyboard import CATALOG_MENU_NEXT, CATALOG_MENU_BACK, PRODUCT_ACTIONS, CHOOSE_PRODUCT_KEYBOARD
from ...storage.local_media_data import TelegramMediaLocalConsolidator


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

    def _generate_callback(self, index: int) -> str:
        return f'{self._prefix.callback}-{index}'

    def _generate_buttons(self, page_data: tuple[tuple[int, Any], ...]) -> tuple[InlineButtonSetting, ...]:
        return tuple(InlineButtonSetting(text=str(i+1),
                                         callback=self._generate_callback(j[0])) for i, j in enumerate(page_data))


    def get_id_by_callback(self, callback: str) -> int:
        return int(callback.replace(f'{self._prefix.callback}-', ''))

    def render_message(self, catalog_service: CatalogMenuService) -> MessageSetting:
        message = self._render_main_body(catalog_service)

        if message.text is None:
            message.text = ''
        message.text = HEADER_CATALOG_TEXT + message.text

        additional_keyboard = ((CATALOG_MENU_BACK if not catalog_service.is_start_page else ()) +
                               (CATALOG_MENU_NEXT if not catalog_service.is_end_page else ()))
        message.keyboard = get_callback_inline_keyboard(*additional_keyboard, row=2,
                                                        keyboard_markup=message.keyboard)

        return message


class CategoryCatalogRenderer(CatalogRenderer):
    def __init__(self, callback_prefix: CallbackSetting):
        super().__init__(callback_prefix)

    def _render_main_body(self, catalog_service) -> MessageSetting:
        page_catalogs = catalog_service.get_page_catalogs()
        text = self._generate_list_catalog(page_catalogs) + HEADER_CATALOG_MENU_TEXT
        keyboard = get_callback_inline_keyboard(*self._generate_buttons(page_catalogs), row=ROW_BUTTON_CATALOG_MENU)

        return MessageSetting(text=text, keyboard=keyboard)

class ChooseProductCatalogRenderer(CatalogRenderer):
    def __init__(self, callback_prefix: CallbackSetting):
        super().__init__(callback_prefix)

    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        page_catalog = catalog_service.get_page_catalogs()
        text = self._generate_list_catalog(page_catalog) + HEADER_CATALOG_MENU_TEXT
        keyboard = get_callback_inline_keyboard(*self._generate_buttons(page_catalog), CHOOSE_PRODUCT_KEYBOARD,
                                                row=1)

        return MessageSetting(text=text, keyboard=keyboard)


class ProductCatalogRenderer(CatalogRenderer):
    def __init__(self, callback_prefix: CallbackSetting, media_consolidator: TelegramMediaLocalConsolidator):
        super().__init__(callback_prefix)

        self._media = media_consolidator

    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        ((index, product), ) = catalog_service.get_page_catalogs()
        text = PRODUCT_INFO_TEXT.insert((product.catalog, product.name_product, product.price, product.description))
        keyboard = get_callback_inline_keyboard(InlineButtonSetting(text='Купить', callback=self._generate_callback(index)))

        return MessageSetting(text=text, keyboard=keyboard, media=tuple(MediaSetting(type_media=obj.type_media,
                                                                                     path=obj.path)
                                                                        for obj in self._media.get_obj_data(*product.media_path))
        if product.media_path is not None else None)

class MediatorChatsRenderer(CatalogRenderer):
    def __init__(self, get_callback_prefix: CallbackSetting, delete_callback_prefix: CallbackSetting):
        super().__init__(get_callback_prefix)

        self._delete_prefix = delete_callback_prefix

    def get_id_by_callback(self, callback: str) -> int:
        if self._prefix.callback in callback:
            return int(callback.replace(f'{self._prefix.callback}-', ''))
        return int(callback.replace(f'{self._delete_prefix}-', ''))

    def _generate_delete_callback(self, index: int) -> str:
        return f'{self._delete_prefix}-{index}'

    def _generate_delete_buttons(self, page_data: tuple[tuple[int, Any]]) -> tuple[InlineButtonSetting, ...]:
        return tuple(InlineButtonSetting(text='Удалить', callback=self._generate_delete_callback(i))
                     for i, _ in page_data)

    def _generate_buttons(self, page_data: tuple[tuple[int, Any], ...]) -> tuple[InlineButtonSetting, ...]:
        return tuple(InlineButtonSetting(text=chat.chat_name, callback=self._generate_callback(i)) for i, chat in page_data)

    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        page_data = catalog_service.get_page_catalogs()

        delete_buttons = self._generate_delete_buttons(page_data)
        chat_buttons = self._generate_buttons(page_data)
        keyboard_data = tuple(item for data in zip(chat_buttons, delete_buttons) for item in data)
        keyboard = get_callback_inline_keyboard(*keyboard_data, row=2)

        return MessageSetting(keyboard=keyboard)

