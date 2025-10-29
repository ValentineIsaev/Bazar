from .handlers_import import *

from bot.storage.redis.storage import FSMStorage
from aiogram.fsm.state import State

from bot.constants.redis_keys import FSMKeys

from bot.utils.message_utils.message_utils import send_message, MessageSetting

from bot.managers.product_managers import ProductCategoryCatalogManager
from bot.managers.catalog_manager import CatalogManager

from bot.components.catalog_renderer import CategoryCatalogRenderer
from bot.utils.message_utils.message_setting_classes import CallbackSetting


async def user_start_handler(bot: Bot, fsm_storage: FSMStorage, state: FSMContext, base_state: State, user_type: str,
                             start_message: MessageSetting):
    if await state.get_state() != base_state:
        await state.set_state(base_state)

    now_type_user = await fsm_storage.get_value(FSMKeys.USERTYPE)
    if now_type_user != user_type:
        await state.update_data({FSMKeys.USERTYPE: user_type})

    await send_message(fsm_storage, bot, start_message)


async def set_category_catalog_manager(catalog_manager: CatalogManager,
                                       product_category_catalog_manager: ProductCategoryCatalogManager,
                                       callback_prefix: CallbackSetting):
    category_catalog = await product_category_catalog_manager.get_category_products()

    await catalog_manager.set_catalog_service(category_catalog)
    await catalog_manager.set_renderer(CategoryCatalogRenderer(callback_prefix))
