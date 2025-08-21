from aiogram import BaseMiddleware


class DIMiddleware(BaseMiddleware):
    def __init__(self, **services):
        self._services = services

    async def __call__(self, handler, event, data: dict):
        for name, value in self._services.items():
            data[name] = value
        return await handler(event, data)
