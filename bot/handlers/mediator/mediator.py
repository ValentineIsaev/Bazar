from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery

from bot.utils.filters import CallbackFilter
from bot.types.utils import CallbackSetting

mediator_router = Router()


@mediator_router.callback_query(CallbackFilter('mediator_chat', 'start'))
async def start_handler(cb: CallbackQuery):
    _, _, action = CallbackSetting(cb.data)

    if action == 'seller':
        pass
    elif action == 'buyer':
        pass
    elif action == 'send_answer':
        pass

