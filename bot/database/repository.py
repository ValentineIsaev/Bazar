from typing import TypeVar, Generic

from .models.mediator_models import ChatMediatorBase

from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

T = TypeVar('T')
class BaseRepository(Generic[T]):
    def __init__(self, session_local: async_sessionmaker[AsyncSession], model: T):
        self._SessionLocal = session_local
        self._model = model

    async def update(self, update_model: T):
        async with self._SessionLocal() as session:
            session.add(update_model)
            await session.commit()

    async def get_all(self) -> tuple[T]:
        async with self._SessionLocal() as session:
            data = await session.execute(select(self._model))
            return data.scalars().all()

    def delete(self, id_model: int):
        pass

    def get_by_id(self, id_model: int) -> T:
        pass


class ProductRepository(BaseRepository):
    pass


class MediatorRepository(BaseRepository[ChatMediatorBase]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChatMediatorBase)

    def __sort_messages(self, messages: tuple[ChatMediatorBase, ...]) -> tuple[tuple[ChatMediatorBase], ...]:
        result = []
        for msg in messages:
            if len(result) == 0:
                result.append([msg])
                continue

            is_added = False
            for index, s_msg in enumerate(result):
                ids_list = (s_msg[0].sender_id, s_msg[0].receiver_id)
                if (msg.sender_id in ids_list or msg.receiver_id in ids_list) and s_msg[0].chat_name == msg.chat_name:
                    result[index].append(msg)
                    is_added = True
                    break

            if not is_added:
                result.append([msg])

        return tuple(map(tuple, result))

    async def get_chats(self, role_user: str, user_id: int) -> tuple[tuple[ChatMediatorBase], ...]:
        stmt = select(self._model).where(
            or_(and_(ChatMediatorBase.receiver_id == user_id, ChatMediatorBase.receiver_role == role_user),
            (and_(ChatMediatorBase.sender_id == user_id, ChatMediatorBase.sender_role == role_user))))

        async with self._SessionLocal() as session:
            result = await session.execute(stmt)

        messages = result.scalars().all()

        return self.__sort_messages(messages)

    async def get_chat(self, chat_id: int) -> tuple[ChatMediatorBase, ...]:
        stmt = select(self._model).where(ChatMediatorBase.chat_id == chat_id)

        async with self._SessionLocal() as session:
            result = await session.execute(stmt)

        return result.scalars().all()
