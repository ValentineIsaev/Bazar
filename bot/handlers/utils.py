from .handlers_import import *

from aiogram.fsm.state import State

from bot.configs.constants import ParamFSM
from bot.utils.helper import get_data_state

from bot.utils.message_utils.message_utils import send_message, MessageSetting

from bot.services.product.services import ProductService
from bot.utils.message_utils.catalog_utils import create_catalog


async def user_start_handler(bot: Bot, state: FSMContext, base_state: State, user_type: str,
                             start_message: MessageSetting):
    if await state.get_state() != base_state:
        await state.set_state(base_state)

    now_user_type = await get_data_state(state, ParamFSM.UserData.TYPE_USER)
    if now_user_type != user_type:
        await state.update_data(**{ParamFSM.UserData.TYPE_USER: user_type})

    await send_message(state, bot, start_message)


async def create_product_catalog(state, choice_callback: str) -> MessageSetting:
    catalog_menu = ProductService.get_product_catalog()
    return await create_catalog(state, choice_callback, catalog_menu)