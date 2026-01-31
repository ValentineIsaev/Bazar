from typing import Any
from abc import abstractmethod

from .base import CatalogRenderer
from .templates.messages import *
from .templates.keyboard import (CATALOG_MENU_NEXT, CATALOG_MENU_BACK, CHOOSE_PRODUCT_KEYBOARD, MEDIATOR_COUNT_BUTTON,
                                 UPDATE_MEDIATOR_CHATS_BUTTON)

from bot.configs.constants import ROW_BUTTON_CATALOG_MENU

from bot.types.utils import MessageSetting, CallbackSetting, MediaSetting, InlineButtonSetting, ParseModes
from bot.types.storage import TelegramMediaLocalConsolidator

from bot.utils.message_utils import get_callback_inline_keyboard

from bot.services.catalog_service import CatalogMenuService


class TelegramCatalogRenderer(CatalogRenderer[MessageSetting, CallbackSetting]):
    def __init__(self, callback_prefix: CallbackSetting):
        self._prefix = callback_prefix

    @abstractmethod
    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        pass

    def _generate_callback(self, index: int) -> CallbackSetting:
        return CallbackSetting.from_str(f'{self._prefix.callback}-{index}')

    def _generate_buttons(self, page_data: tuple[tuple[int, Any], ...]) -> tuple[InlineButtonSetting, ...]:
        return tuple(InlineButtonSetting(text=str(data),
                                         callback=self._generate_callback(i)) for i, data in page_data)


    def get_id_by_callback(self, callback: CallbackSetting) -> int:
        return int(callback.callback.replace(f'{self._prefix.callback}-', ''))

    def render_message(self, catalog_service: CatalogMenuService) -> MessageSetting:
        message = self._render_main_body(catalog_service)

        if message.text is None:
            message.text = ''
        message.text = message.text + HEADER_CATALOG_TEXT

        additional_keyboard = ((CATALOG_MENU_BACK if not catalog_service.is_start_page else ()) +
                               (CATALOG_MENU_NEXT if not catalog_service.is_end_page else ()))
        message.keyboard = get_callback_inline_keyboard(*additional_keyboard, row=2,
                                                        keyboard_markup=message.keyboard)

        return message


class SortCategoryCatalogRenderer(TelegramCatalogRenderer):
    def __init__(self, callback_prefix: CallbackSetting):
        super().__init__(callback_prefix)

    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        page_data = catalog_service.get_page_catalogs()
        keyboard = get_callback_inline_keyboard(*self._generate_buttons(page_data), row=ROW_BUTTON_CATALOG_MENU)
        return MessageSetting(text=SORT_SELLER_PRODUCT_TEXT, keyboard=keyboard, parse_mode=ParseModes.MARKDOWN_V2)

class BuyerCategoryCatalogRenderer(TelegramCatalogRenderer):
    def __init__(self, callback_prefix: CallbackSetting):
        super().__init__(callback_prefix)

    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        page_data = catalog_service.get_page_catalogs()
        keyboard = get_callback_inline_keyboard(*self._generate_buttons(page_data), row=ROW_BUTTON_CATALOG_MENU)
        return MessageSetting(text=CHOICE_BUYER_CATALOG_TEXT, keyboard=keyboard, parse_mode=ParseModes.MARKDOWN_V2)


class CategoryCatalogRenderer(TelegramCatalogRenderer):
    def __init__(self, callback_prefix: CallbackSetting):
        super().__init__(callback_prefix)

    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        page_data = catalog_service.get_page_catalogs()
        keyboard = get_callback_inline_keyboard(*self._generate_buttons(page_data), row=ROW_BUTTON_CATALOG_MENU)
        return MessageSetting(text=HEADER_CATALOG_MENU_TEXT, keyboard=keyboard)


class AddProductCatalogRenderer(TelegramCatalogRenderer):
    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        page_data = catalog_service.get_page_catalogs()
        keyboard = get_callback_inline_keyboard(*self._generate_buttons(page_data), row=ROW_BUTTON_CATALOG_MENU)
        return MessageSetting(text=ADD_CATALOG_TO_PRODUCT+HEADER_CATALOG_MENU_TEXT, keyboard=keyboard,
                              parse_mode=ParseModes.MARKDOWN_V2)


class ChooseProductCatalogRenderer(TelegramCatalogRenderer):
    def __init__(self, callback_prefix: CallbackSetting):
        super().__init__(callback_prefix)

    def _generate_buttons(self, page_data: tuple[tuple[int, Any], ...]) -> tuple[InlineButtonSetting, ...]:
        return tuple(InlineButtonSetting(text=f'{product.name_product} ({product.catalog})',
                                         callback=self._generate_callback(i)) for i, product in page_data)

    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        page_data = catalog_service.get_page_catalogs()
        keyboard = get_callback_inline_keyboard(*self._generate_buttons(page_data), CHOOSE_PRODUCT_KEYBOARD,
                                                row=1)

        return MessageSetting(text=CHOOSE_PRODUCT_SELLER_TEXT, keyboard=keyboard, parse_mode=ParseModes.MARKDOWN_V2)


class ProductCatalogRenderer(TelegramCatalogRenderer):
    def __init__(self, callback_prefix: CallbackSetting, media_consolidator: TelegramMediaLocalConsolidator):
        super().__init__(callback_prefix)

        self._media = media_consolidator

    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        ((index, product), ) = catalog_service.get_page_catalogs()
        text = PRODUCT_INFO_TEXT.insert((product.catalog, product.name_product, product.description, product.price))
        keyboard = get_callback_inline_keyboard(InlineButtonSetting(text='Подробнее ↘', callback=self._generate_callback(index)))

        return MessageSetting(text=text, keyboard=keyboard, media=tuple(MediaSetting(type_media=obj.type_media,
                                                                                     path=obj.path)
                                                                        for obj in self._media.get_obj_data(*product.media_path))
        if product.media_path is not None else None,
                              parse_mode=ParseModes.MARKDOWN_V2)


class MediatorChatsRenderer(TelegramCatalogRenderer):
    def __init__(self, get_callback_prefix: CallbackSetting, delete_callback_prefix: CallbackSetting):
        super().__init__(get_callback_prefix)

        self._delete_prefix = delete_callback_prefix

    def get_id_by_callback(self, callback: CallbackSetting) -> int:
        if self._prefix.callback in callback.callback:
            return int(callback.callback.replace(f'{self._prefix.callback}-', ''))
        return int(callback.callback.replace(f'{self._delete_prefix}-', ''))

    def _generate_delete_callback(self, index: int) -> CallbackSetting:
        return CallbackSetting.from_str(f'{self._delete_prefix}-{index}')

    def _generate_delete_buttons(self, page_data: tuple[tuple[int, Any]]) -> tuple[InlineButtonSetting, ...]:
        return tuple(InlineButtonSetting(text='Удалить 🗑', callback=self._generate_delete_callback(i))
                     for i, _ in page_data)

    def _generate_buttons(self, page_data: tuple[tuple[int, Any], ...]) -> tuple[InlineButtonSetting, ...]:
        return tuple(InlineButtonSetting(text=MEDIATOR_COUNT_BUTTON.insert((chat.count_update,)) + str(chat.chat_name)
                                              if chat.count_update > 0
        else str(chat.chat_name), callback=self._generate_callback(i)) for i, chat in page_data)

    def _render_main_body(self, catalog_service: CatalogMenuService) -> MessageSetting:
        page_data = catalog_service.get_page_catalogs()

        delete_buttons = self._generate_delete_buttons(page_data)
        chat_buttons = self._generate_buttons(page_data)
        keyboard_data = tuple(item for data in zip(chat_buttons, delete_buttons) for item in data)
        update_keyboard = get_callback_inline_keyboard(UPDATE_MEDIATOR_CHATS_BUTTON, row=1)
        keyboard = get_callback_inline_keyboard(*keyboard_data, row=2,
                                                keyboard_markup=update_keyboard)

        return MessageSetting(text=MEDIATOR_CHATS_MENU_TEXT, keyboard=keyboard, parse_mode=ParseModes.MARKDOWN_V2)

