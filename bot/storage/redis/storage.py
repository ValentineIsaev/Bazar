from abc import ABC, abstractmethod
from typing import Any

from aiogram.fsm.context import FSMContext


class Storage(ABC):
    @abstractmethod
    async def get_value(self, key: str):
        pass

    @abstractmethod
    async def get_data(self, *keys: str):
        pass

    @abstractmethod
    async def update_data(self, **data: dict[str, Any]):
        pass

    @abstractmethod
    async def update_value(self, key: str, value):
        pass

    @abstractmethod
    async def get_all_data(self):
        pass


class FSMStorage(Storage):
    def __init__(self, state: FSMContext):
        self._state = state

    async def get_value(self, key: str):
        return await self._state.get_value(key)

    async def get_data(self, *keys: str):
        data = await self._state.get_data()
        return tuple(data.get(key) for key in keys)

    async def update_data(self, **data: dict[str, Any]):
        await self._state.update_data(data)

    async def update_value(self, key: str, value):
        await self._state.update_data({key: value})

    async def get_all_data(self):
        return await self._state.get_data()