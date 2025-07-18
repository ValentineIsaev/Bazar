from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.configs.constants import ParamFSM
from bot.utils.keyboard_utils import parse_callback

class TypeUserFilter(BaseFilter):
    def __init__(self, type_user: str):
        self._user = type_user

    async def __call__(self, event: Message | CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        type_user = user_data.get(ParamFSM.UserData.TYPE_USER)

        return type_user == self._user


class CallbackFilter(BaseFilter):
    def __init__(self, scope: str=None, subscope: str=None, action: str=None):
        self._scope = scope
        self._subscope = subscope
        self._action = action


    async def __call__(self, cb: CallbackQuery):
        scope, subscope, action = parse_callback(cb.data)
        return ((self._scope is None or scope == self._scope) and
                (self._subscope is None or subscope == self._subscope) and
                (self._action is None or action == self._action))
