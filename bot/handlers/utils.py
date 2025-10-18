from .handlers_import import *

from bot.storage.redis.storage import Storage
from aiogram.fsm.state import State

from bot.constants.redis_keys import UserSessionKeys, FSMKeys
from bot.utils.helper import get_data_state

from bot.utils.message_utils.media_messages_utils import delete_media_message
from bot.utils.message_utils.message_utils import send_message, MessageSetting, delete_bot_message

from bot.managers.product_managers import ProductManager

from bot.components.catalog_render import ProductCatalogHierarchyManager


async def user_start_handler(bot: Bot, storage: Storage, state: FSMContext, base_state: State, user_type: str,
                             start_message: MessageSetting):
    if await state.get_state() != base_state:
        await state.set_state(base_state)

    now_type_user = await state.get_value(FSMKeys.USERTYPE)
    if now_type_user != user_type:
        await state.update_data({FSMKeys.USERTYPE: user_type})

    await send_message(storage, bot, start_message)


async def create_menu_catalog(state: FSMContext, choice_callback: str,
                              product_manager: ProductManager) -> MessageSetting:
    catalog_service = product_manager.get_catalogs()
    catalog_manager = ProductCatalogHierarchyManager(catalog_service, choice_callback)

    await state.update_data(**{FSMKeys.CATALOG_MANAGER: catalog_manager})

    return catalog_manager.create_message()

async def send_catalog_message(storage: Storage, bot: Bot, message: MessageSetting):
    is_send_new = False

    await delete_media_message(storage, bot)
    if message.media is not None or message.cache_media is not None:
        await delete_bot_message(storage, bot)
        is_send_new = True

    await send_message(storage, bot, message, is_send_new)

async def repack_choice_catalog_data(state: FSMContext, callback: str):
    catalog_manager: ProductCatalogHierarchyManager
    (catalog_manager,) = await get_data_state(state, FSMKeys.CATALOG_MANAGER)
    catalog_callback, catalog_menu = catalog_manager.choice_callback, catalog_manager.catalog

    number_catalog = int(callback.replace(f'{catalog_callback}-', ''))

    selected_catalog = catalog_menu[number_catalog]
    return selected_catalog