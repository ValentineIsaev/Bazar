from aiogram import Bot
from aiogram.fsm.context import FSMContext

from .render_data_strategies import CatalogRender, MenuCatalogRender, ProductCatalogRender
from .messages import HEADER_CATALOG_TEXT

from bot.utils.message_utils.message_setting_classes import MessageSetting
from bot.utils.message_utils.keyboard_utils import (create_callback_inline_keyboard, add_callback_inline_keyboard,
                                                    InlineButtonSetting, create_callback)
from bot.utils.helper import get_data_state
from bot.utils.message_utils.message_utils import delete_bot_message, send_message
from bot.utils.message_utils.media_messages_utils import send_media_message, send_cached_media_message, delete_media_message

from bot.services.product.services import CatalogMenuService
from bot.configs.constants import ParamFSM


CATALOG_MENU_NEXT = (InlineButtonSetting(text='Вперед', callback=create_callback('catalog_menu',
                                                                                'scroll',
                                                                                'next')),)
CATALOG_MENU_BACK = (InlineButtonSetting(text='Назад', callback=create_callback('catalog_menu',
                                                                                'scroll',
                                                                                'back')),)


async def create_catalog_message(state: FSMContext) -> MessageSetting:
    catalog_menu: CatalogMenuService; data_render: CatalogRender
    catalog_menu, data_render = await get_data_state(state,ParamFSM.BotMessagesData.CatalogData.CATALOG_MENU,
                                                     ParamFSM.BotMessagesData.CatalogData.RENDER_CATALOG_DATA_CLASS)

    catalog = catalog_menu.get_catalogs()
    message = await data_render.rendering_data(state, catalog)

    if message.text is None:
        message.text = ''
    message.text = HEADER_CATALOG_TEXT + message.text

    additional_keyboard = ((CATALOG_MENU_BACK if not catalog_menu.is_start_page else ()) +
                           (CATALOG_MENU_NEXT if not catalog_menu.is_end_page else ()))
    keyboard = message.keyboard
    message.keyboard = create_callback_inline_keyboard(*additional_keyboard, row=2) if keyboard is None \
        else add_callback_inline_keyboard(keyboard, *additional_keyboard,row=2)

    return message


async def send_catalog_message(state: FSMContext, bot: Bot, message: MessageSetting):
    is_send_new = False
    await delete_media_message(state)
    if message.media is not None or message.cache_media is not None:
        await delete_bot_message(state)
        is_send_new = True

        if message.media is not None:
            await send_media_message(state, bot, MessageSetting(media=message.media))
        elif message.cache_media is not None:
            await send_cached_media_message(state, bot, MessageSetting(cache_media=message.cache_media))

    await send_message(state, bot, message, is_send_new)


async def repack_choice_catalog_data(callback: str, state: FSMContext):
    catalog_menu: CatalogMenuService
    catalog_menu, catalog_callback  = await get_data_state(state, ParamFSM.BotMessagesData.CatalogData.CATALOG_MENU,
                                           ParamFSM.BotMessagesData.CatalogData.CATALOG_MENU_CALLBACK)

    number_catalog = int(callback.replace(f'{catalog_callback}-', ''))

    selected_catalog = catalog_menu.get_catalogs()[number_catalog]
    return selected_catalog

async def create_catalog(state: FSMContext, choice_callback: str, catalog_menu: CatalogMenuService) -> MessageSetting:
    await state.update_data(**{ParamFSM.BotMessagesData.CatalogData.CATALOG_MENU: catalog_menu,
                               ParamFSM.BotMessagesData.CatalogData.CATALOG_MENU_CALLBACK: choice_callback,
                               ParamFSM.BotMessagesData.CatalogData.RENDER_CATALOG_DATA_CLASS: MenuCatalogRender()})

    return await create_catalog_message(state)

async def create_product_catalog(state: FSMContext, bot: Bot, catalog_menu: CatalogMenuService):
    await state.update_data(**{ParamFSM.BotMessagesData.CatalogData.CATALOG_MENU: catalog_menu,
                               ParamFSM.BotMessagesData.CatalogData.RENDER_CATALOG_DATA_CLASS: ProductCatalogRender()})

    await send_catalog_message(state, bot, await create_catalog_message(state))
