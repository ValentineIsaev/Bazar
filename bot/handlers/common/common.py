from bot.constants.redis_keys import FSMKeys, UserSessionKeys
from bot.storage.redis import Storage, FSMStorage
from bot.utils.message_utils.message_utils import send_message

from .messages import *
from ..handlers_import import *

common_router = Router()
unexpected_router = Router()


@common_router.message(Command('start'))
async def handler_start(msg: Message, storage: Storage, fsm_storage: FSMStorage):
    user_data = await fsm_storage.get_all_data()
    print(user_data)
    if not user_data:
        await storage.update_data(**{UserSessionKeys.CHAT_ID: msg.chat.id,
                                     UserSessionKeys.USERNAME: msg.from_user.first_name})
        await fsm_storage.update_value(FSMKeys.USERTYPE, UserTypes.DEFAULTS)
        await send_message(storage, msg.bot, START_MESSAGE)
    else:
        if FSMKeys.USERTYPE not in user_data.keys():
            raise ValueError('Error in logic')
        await send_message(storage, msg.bot, DEFAULT_MESSAGES[user_data[FSMKeys.USERTYPE]])


@common_router.message(Command('help'))
async def send_help(message: Message, storage: Storage):
    await send_message(storage, message.bot, HELP_MESSAGE)


@unexpected_router.callback_query()
async def errors_callback(cb: CallbackQuery, fsm_storage: FSMStorage):
    type_user = await fsm_storage.get_value(FSMKeys.USERTYPE)
    print(type_user)
    print(f'Errors callback: {cb.data}')


@unexpected_router.message()
async def error_message(msg: Message, state: FSMContext):
    print('Error message', msg)
    now_state = await state.get_state()
    print('state', now_state)
