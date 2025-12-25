from typing import TypeVar, Generic
from bot.configs.constants import UserTypes

from .models import UserBase, ProductBase, MediatorChatBase, MediatorMessageBase, MoneyBalanceBase

from sqlalchemy import select, or_, and_, delete
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

    async def get_chats(self, user_id: int, user_role: str) -> tuple[T, ...]:
        field = self._model.buyer_user_id if user_role == UserTypes.BUYER else self._model.seller_user_id
        stmt = select(self._model).where(field == str(user_id))
        result = await self._session.execute(stmt)

        return tuple(result.scalars().all())

    async def start_chat(self, chat_data: T) -> T:
        self._session.add(chat_data)
        await self._session.commit()
        await self._session.refresh(chat_data)

        return chat_data

    async def delete_chat(self, chat_id: str):
        stmt = delete(self._model).where(self._model.mediator_chat_id == chat_id)
        await self._session.execute(stmt)
        await self._session.commit()


class MessagesMediatorRepository(BaseRepository[MediatorMessageBase]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MediatorMessageBase)

    async def get_chat_msgs(self, chat_id: str) -> tuple[T, ...]:
        stmt = select(self._model).where(self._model.mediator_chat_id == chat_id)
        result = await self._session.execute(stmt)

        return tuple(result.scalars().all())

    async def send_msg(self, msg: MediatorMessageBase):
        self._session.add(msg)
        await self._session.commit()

    async def delete_msgs(self, chat_id: str):
        stmt = delete(self._model).where(self._model.mediator_chat_id == chat_id)
        await self._session.execute(stmt)
        await self._session.commit()
