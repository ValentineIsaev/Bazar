from typing import TypeVar, Generic

from .models import UserBase, ProductBase, MediatorChatBase, MediatorMessageBase, MoneyBalanceBase

from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: T):
        self._session = session
        self._model = model

    async def update(self, update_model: T):
        self._session.add(update_model)
        await self._session.commit()

    async def get_all(self) -> tuple[T]:
        data = await self._session.execute(select(self._model))
        return data.scalars().all()

    def delete(self, id_model: int):
        pass

    def get_by_id(self, id_model: int) -> T:
        pass


class ProductsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductBase)


class ChatsMediatorRepository(BaseRepository[MediatorChatBase]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MediatorChatBase)
