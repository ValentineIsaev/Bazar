from bot.handlers.handlers_import import *

from ..templates.messages import *
from ..templates.keyboard import *
from ..templates.configs import BASE_STATE

from bot.configs.constants import ParamFSM, UserTypes
from bot.utils.helper import get_data_state
from bot.handlers.utils import user_start_handler

router = Router()

@router.message(Command('buyer'))
async def buyer_base(msg: Message, state: FSMContext):
    user_data = await get_data_state(state, ParamFSM.UserData.NAME)
    msg_text = START_MESSAGE_TEXT.insert(user_data)
    new_message = MessageSetting(text=msg_text, keyboard=START_KEYBOARD)
    await user_start_handler(msg.bot, state, BASE_STATE, UserTypes.BUYER, new_message)