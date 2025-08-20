from .handlers_import import *

from aiogram.fsm.state import State

from bot.configs.constants import ParamFSM
from bot.utils.helper import get_data_state

from bot.utils.message_utils.message_utils import send_message, MessageSetting

from bot.services.product.services import ProductService

from bot.managers.catalog_manager.catalog_managers import ProductCatalogHierarchyManager


async def user_start_handler(bot: Bot, state: FSMContext, base_state: State, user_type: str,
                             start_message: MessageSetting):
    if await state.get_state() != base_state:
        await state.set_state(base_state)

    now_user_type = await get_data_state(state, ParamFSM.UserData.TYPE_USER)
    if now_user_type != user_type:
        await state.update_data(**{ParamFSM.UserData.TYPE_USER: user_type})

    await send_message(state, bot, start_message)


async def create_menu_catalog(state: FSMContext, choice_callback: str,
                              product_service: ProductService) -> MessageSetting:
    catalog_service = product_service.get_product_catalog()
    catalog_manager = ProductCatalogHierarchyManager(catalog_service, choice_callback)

    await state.update_data(**{ParamFSM.BotMessagesData.CATALOG_MANAGER: catalog_manager})

    return catalog_manager.create_message()

async def repack_choice_catalog_data(state: FSMContext, callback: str):
    catalog_manager: ProductCatalogHierarchyManager
    (catalog_manager,) = await get_data_state(state, ParamFSM.BotMessagesData.CATALOG_MANAGER)
    catalog_callback, catalog_menu = catalog_manager.choice_callback, catalog_manager.catalog

    number_catalog = int(callback.replace(f'{catalog_callback}-', ''))

    selected_catalog = catalog_menu.get_catalogs()[number_catalog]
    return selected_catalog