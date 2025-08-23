from aiogram import F
from aiogram.filters import StateFilter

from bot.handlers.utils import user_start_handler
from bot.handlers.handlers_import import *
from bot.handlers.seller.templates.configs import BASE_STATE

from bot.configs.constants import UserTypes

from bot.constants.callback import PASS_CALLBACK

from bot.utils.message_utils.message_utils import MessageSetting
from bot.managers.session_manager.session import UserSession

from bot.handlers.seller.templates.messages import START_MESSAGE
from bot.handlers.seller.templates.keyboards import MENU_KEYBOARD

router = Router()

@router.message(Command('seller'))
@router.callback_query(StateFilter(BASE_STATE), F.data == PASS_CALLBACK)
async def send_seller_menu(msg: Message, state: FSMContext, session: UserSession):
    msg_data = (msg.from_user.first_name, 0, 0)
    new_msg = MessageSetting(text=START_MESSAGE.insert(msg_data), keyboard=MENU_KEYBOARD)
    await user_start_handler(msg.bot, session, state, BASE_STATE, UserTypes.SELLER, new_msg)
