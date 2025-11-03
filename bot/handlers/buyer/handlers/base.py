from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..templates.messages import *
from ..templates.keyboard import *
from ..templates.configs import BASE_STATE

from bot.constants.redis_keys import UserSessionKeys
from bot.storage.redis import FSMStorage
from bot.configs.constants import UserTypes
from bot.handlers.utils import user_start_handler
from bot.types.utils import MessageSetting


router = Router()

@router.message(Command('buyer'))
async def buyer_base(msg: Message, state: FSMContext, fsm_storage: FSMStorage):
    user_data = (await fsm_storage.get_value(UserSessionKeys.USERNAME),)
    msg_text = START_MESSAGE_TEXT.insert(user_data)
    new_message = MessageSetting(text=msg_text, keyboard=START_KEYBOARD)
    await user_start_handler(msg.bot, fsm_storage, state, BASE_STATE, UserTypes.BUYER, new_message)