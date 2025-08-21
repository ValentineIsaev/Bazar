from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext


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
        for name, value in self._services:
            service = await state.get_value(name)
            if service is None:
                service = value()
                await state.update_data(**{name: service})

            data[name] = service

        return await handler(event, data)
