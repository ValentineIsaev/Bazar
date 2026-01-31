from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from .messages import *

from bot.constants.redis_keys import StorageKeys
from bot.types.storage import FSMStorage
from bot.utils.message_utils import send_message
from bot.handlers.helpers import processing_start


common_router = Router()


@common_router.message(Command('start'))
async def handler_start(msg: Message, fsm_storage: FSMStorage):
    print('start')
    await processing_start(fsm_storage, msg, START_MESSAGE)


@common_router.message(Command('help'))
async def send_help(message: Message, fsm_storage: FSMStorage):
    await send_message(fsm_storage, message.bot, HELP_MESSAGE)


@common_router.callback_query()
async def errors_callback(cb: CallbackQuery, fsm_storage: FSMStorage):
    type_user = await fsm_storage.get_value(StorageKeys.USERTYPE)
    print(type_user)
    print(f'Errors callback: {cb.data}')


@common_router.message()
async def error_message(msg: Message, state: FSMContext):
    print('Error message', msg)
    now_state = await state.get_state()
    print('state', now_state)
