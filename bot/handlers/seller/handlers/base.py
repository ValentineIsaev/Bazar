from aiogram import F, Router
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..messages import START_TEXT_MSG
from ..keyboards import MENU_KEYBOARD
from ..fsm import SellerStates

from bot.constants.redis_keys import StorageKeys
from bot.constants.callback import SELLER_MENU_CALLBACK
from bot.constants.user_constants import TypesUser

from bot.types.storage import FSMStorage
from bot.types.utils import MessageSetting, CallbackSetting

from bot.utils.filters import CallbackFilter

from bot.handlers.helpers import processing_start, get_hello_text_msg, get_menu_keyboard


router = Router()


async def _send_seller_menu(msg: Message, user_name: str, mediator_manager, state: FSMContext,
                            fsm_storage: FSMStorage, is_delete_msg=True):
    other_data = 0
    balance = 1000
    hello_text_msg = get_hello_text_msg(user_name)
    menu_keyboard = await get_menu_keyboard(*MENU_KEYBOARD, mediator_manager=mediator_manager,
                                            user_id=msg.from_user.id, user_role=TypesUser.SELLER)
    new_msg = MessageSetting(text=hello_text_msg + START_TEXT_MSG.insert((other_data, balance)), keyboard=menu_keyboard)

    await processing_start(fsm_storage, msg, new_msg, state=state, new_type_user=TypesUser.SELLER,
                           new_state=SellerStates.seller_menu, is_delete_msg=is_delete_msg)


@router.message(Command('seller'))
async def send_seller_menu_command(msg: Message, state: FSMContext, fsm_storage: FSMStorage,
                           mediator_manager):
    await _send_seller_menu(msg, msg.from_user.first_name, mediator_manager, state, fsm_storage)

@router.callback_query(CallbackFilter(*CallbackSetting.decode_callback(SELLER_MENU_CALLBACK.callback)))
async def send_seller_menu_callback_query(cb: CallbackQuery, state: FSMContext, fsm_storage: FSMStorage,
                                          mediator_manager):
    user_name = await fsm_storage.get_value(StorageKeys.USERNAME)
    await _send_seller_menu(cb.message, user_name, mediator_manager, state, fsm_storage, is_delete_msg=False)
