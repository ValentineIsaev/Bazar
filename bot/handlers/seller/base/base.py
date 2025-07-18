from aiogram import F
from aiogram.filters import StateFilter
from bot.handlers.handlers_import import *
from bot.handlers.seller.configs import BASE_STATE

from bot.configs.constants import UserTypes, ParamFSM, PASS_CALLBACK
from bot.utils.message_utils import MessageSetting, insert_text, send_message
from bot.utils.helper import get_data_state

from .messages import START_MESSAGE
from .keyboards import MENU_KEYBOARD

router = Router()

@router.message(Command('seller'))
@router.callback_query(StateFilter(BASE_STATE), F.data == PASS_CALLBACK)
async def send_seller_menu(msg: Message, state: FSMContext):
    if await state.get_state() != BASE_STATE:
        await state.set_state(BASE_STATE)
        await state.update_data(**{ParamFSM.UserData.TYPE_USER: UserTypes.SELLER})

    msg_data = await get_data_state(state, ParamFSM.UserData.NAME,ParamFSM.UserData.RATING,
                                    ParamFSM.UserData.MONEY)
    new_msg = MessageSetting(text=insert_text(START_MESSAGE, msg_data), keyboard=MENU_KEYBOARD)
    await send_message(state, msg.bot, new_msg)
