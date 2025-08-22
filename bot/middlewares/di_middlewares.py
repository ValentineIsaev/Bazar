from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.managers.session_manager.session import SessionManager


class DIMiddleware(BaseMiddleware):
    def __init__(self, **services):
        self._services = services

    async def __call__(self, handler, event, data: dict):
        for name, value in self._services.items():
            data[name] = value
        return await handler(event, data)


class DIUserMiddleware(DIMiddleware):
    async def __call__(self, handler, event, data: dict):
        state: FSMContext = data.get('state')
        for name, value in self._services.items():
            service = await state.get_value(name)
            if service is None:
                service = value()
                await state.update_data(**{name: service})

            data[name] = service

        return await handler(event, data)

class UserSessionMiddleware(BaseMiddleware):
    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    async def __call__(self, handler, event: Message | CallbackQuery, data: dict):
        user_id = event.from_user.id
        data['session'] = self._session_manager.get_session(user_id)

        return await handler(event, data)
