from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..messages import *
from ..keyboard import *
from ..fsm import BuyerStates

from bot.constants.user_constants import TypesUser

from bot.storage.redis import FSMStorage
from bot.types.utils import MessageSetting
from bot.handlers.helpers import processing_start, get_hello_text_msg, get_menu_keyboard


router = Router()

@router.message(Command('buyer'))
async def buyer_base(msg: Message, state: FSMContext, fsm_storage: FSMStorage,
                     mediator_manager):
    balance = 1000
    hello_text_msg = get_hello_text_msg(msg.from_user.first_name)
    msg_text = START_MESSAGE_TEXT.insert((balance,))
    keyboard = await get_menu_keyboard(*START_KEYBOARD, mediator_manager=mediator_manager, user_id=msg.from_user.id,
                                 user_role=TypesUser.BUYER)
    new_message = MessageSetting(text=hello_text_msg+msg_text, keyboard=keyboard)
    await processing_start(fsm_storage, msg, new_message, state, TypesUser.BUYER, new_state=BuyerStates.main_menu)