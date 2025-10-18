from aiogram import BaseMiddleware
from bot.storage.redis import FSMStorage

class DIMiddleware(BaseMiddleware):
    def __init__(self, **dependencies: dict):
        self._dependencies = dependencies

    async def __call__(self, handel, event, data):
        state = data['state']
        data['storage'] = FSMStorage(state)
        data['fsm_storage'] = FSMStorage(state)
        for name, dependence in self._dependencies.items():
            data[name] = dependence(data)

        return await handel(event, data)

