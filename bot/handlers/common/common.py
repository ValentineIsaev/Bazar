from aiogram.filters import StateFilter

from bot.configs.constants import ParamFSM
from bot.utils.message_utils import send_message

from .messages import *
from ..handlers_import import *

common_router = Router()
unexpected_router = Router()


@common_router.message(Command('start'))
async def handler_start(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    if not user_data:
        await state.update_data(**{ParamFSM.BotMessagesData.CHAT_ID: msg.chat.id,
                                   ParamFSM.UserData.TYPE_USER: UserTypes.DEFAULTS,
                                   ParamFSM.UserData.MONEY: 0, ParamFSM.UserData.RATING: 0,
                                   ParamFSM.UserData.NAME: msg.from_user.first_name})
        await send_message(state, msg.bot, START_MESSAGE)
    else:
        if ParamFSM.UserData.TYPE_USER not in user_data.keys():
            raise ValueError('Error in logic')
        await send_message(state, msg.bot, DEFAULT_MESSAGES[user_data[ParamFSM.TYPE_USER]])


@common_router.message(Command('help'))
async def send_help(message: Message, state: FSMContext):
    await send_message(state, message.bot, HELP_MESSAGE)


@unexpected_router.callback_query()
async def errors_callback(cb: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    print(user_data.get(ParamFSM.UserData.TYPE_USER))
    print(f'Errors callback: {cb.data}')


@unexpected_router.message()
async def error_message(msg: Message):
    print('Error message', msg)
