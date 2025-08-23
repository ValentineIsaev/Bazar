from bot.constants.redis_keys import FSMKeys, UserSessionKeys
from bot.managers.session_manager.session import UserSession
from bot.utils.message_utils.message_utils import send_message

from .messages import *
from ..handlers_import import *

common_router = Router()
unexpected_router = Router()


@common_router.message(Command('start'))
async def handler_start(msg: Message, session: UserSession):
    user_data = await session.get_all_data()
    print(user_data)
    if not user_data:
        await session.set_values(**{UserSessionKeys.CHAT_ID: msg.chat.id,
                                   UserSessionKeys.USERTYPE: UserTypes.DEFAULTS,
                                   UserSessionKeys.USERNAME: msg.from_user.first_name})
        await send_message(session, msg.bot, START_MESSAGE)
    else:
        if UserSessionKeys.USERTYPE not in user_data.keys():
            raise ValueError('Error in logic')
        await send_message(session, msg.bot, DEFAULT_MESSAGES[user_data[UserSessionKeys.USERTYPE]])


@common_router.message(Command('help'))
async def send_help(message: Message, session: UserSession):
    await send_message(session, message.bot, HELP_MESSAGE)


@unexpected_router.callback_query()
async def errors_callback(cb: CallbackQuery, session: UserSession):
    type_user = session.get_value(UserSessionKeys.USERTYPE)
    print(type_user)
    print(f'Errors callback: {cb.data}')


@unexpected_router.message()
async def error_message(msg: Message, state: FSMContext):
    print('Error message', msg)
    now_state = await state.get_state()
    print('state', now_state)
