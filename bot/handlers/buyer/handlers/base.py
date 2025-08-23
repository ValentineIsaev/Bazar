from bot.handlers.handlers_import import *

from ..templates.messages import *
from ..templates.keyboard import *
from ..templates.configs import BASE_STATE

from bot.constants.redis_keys import UserSessionKeys
from bot.managers.session_manager.session import UserSession
from bot.configs.constants import UserTypes
from bot.handlers.utils import user_start_handler

router = Router()

@router.message(Command('buyer'))
async def buyer_base(msg: Message, state: FSMContext, session: UserSession):
    user_data = (await session.get_value(UserSessionKeys.USERNAME),)
    msg_text = START_MESSAGE_TEXT.insert(user_data)
    new_message = MessageSetting(text=msg_text, keyboard=START_KEYBOARD)
    await user_start_handler(msg.bot, session, state, BASE_STATE, UserTypes.BUYER, new_message)