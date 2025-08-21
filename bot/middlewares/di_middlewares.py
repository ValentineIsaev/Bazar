from aiogram import BaseMiddleware


class DIMiddleware(BaseMiddleware):
    def __init__(self, **di_data):
        self._di_data = di_data

    async def __call__(self, handler, event, data: dict):
        for name, value in self._di_data.items():
            data[name] = value
        return await handler(event, data)
