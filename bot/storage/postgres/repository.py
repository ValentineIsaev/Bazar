from typing import TypeVar, Generic
from bot.configs.constants import UserTypes

from .models import UserBase, ProductBase, MediatorChatBase, MediatorMessageBase, MoneyBalanceBase

from sqlalchemy import select, or_, and_, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: T):
        self._session = session
        self._model = model

    async def get_all(self) -> tuple[T]:
        data = await self._session.execute(select(self._model))
        return data.scalars().all()


class ProductsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductBase)

    async def get_products_by_user_id(self, user_id: int) -> tuple[T, ...]:
        stmt = select(self._model).where(
            self._model.autor_id == str(user_id)
        )

        result = await self._session.execute(stmt)
        return tuple(result.scalars().all())

    async def get_product_by_id(self, product_id: str) -> tuple[T, ...]:
        pass

    async def get_products_by_catalog(self, catalog: str) -> tuple[T, ...]:
        stmt = select(self._model).where(
            self._model.catalog == catalog
        )

        result = await self._session.execute(stmt)
        return tuple(result.scalars().all())

    async def create_product(self, product: T):
        self._session.add(product)
        await self._session.commit()

    async def delete_product(self, product_id: int):
        stmt = delete(self._model).where(
            self._model.product_id == product_id
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def update_product(self, product: T):
        print(product.id)
        stmt = update(self._model).where(
            self._model.id == product.id
        ).values(**{k: v for k, v in product.__dict__.items() if not k.startswith('_')})
        await self._session.execute(stmt)
        await self._session.commit()


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
        stmt = delete(self._model).where(
            self._model.mediator_chat_id == chat_id
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def is_chat_exist(self, chat: MediatorChatBase) -> tuple[bool, T]:
        stmt = select(self._model).where(
            and_(
                self._model.seller_user_id == chat.seller_user_id,
                self._model.product_id == chat.product_id,
                self._model.buyer_user_id == chat.buyer_user_id
            )
        )

        result = await self._session.execute(stmt)
        data = result.scalars().all()
        return bool(data), data[0] if len(data) > 0 else data

    async def get_chat_by_id(self, chat_id: str) -> MediatorChatBase:
        stmt = select(self._model).where(
            self._model.mediator_chat_id == chat_id
        )
        result = await self._session.execute(stmt)

        return tuple(result.scalars().all())[0]


class MessagesMediatorRepository(BaseRepository[MediatorMessageBase]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MediatorMessageBase)

    async def get_chat_msgs(self, chat_id: str) -> tuple[T, ...]:
        stmt = select(self._model).where(
            self._model.mediator_chat_id == chat_id
        ).order_by(
            self._model.sender_date
        )

        result = await self._session.execute(stmt)
        return tuple(result.scalars().all())

    async def get_count_new_msgs(self, chat_id: str, user_id: int) -> int:
        stmt = select(func.count()).where(
            and_(
                self._model.mediator_chat_id == chat_id,
                self._model.sender_id != str(user_id),
                self._model.is_recipient_read == False
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def recipient_msgs(self, msgs_ids: list[int, ...], user_id: int):
        stmt = update(self._model).where(
            and_(
                self._model.id.in_(msgs_ids),
                self._model.sender_id != str(user_id),
                self._model.is_recipient_read == False
            )
        ).values(
            is_recipient_read=True
        )

        await self._session.execute(stmt)
        await self._session.commit()

    async def get_new_msgs(self, chat_id: str, user_id: int) -> tuple[T, ...]:
        stmt = select(self._model).where(
            and_(
                self._model.mediator_chat_id == chat_id,
                self._model.sender_id != str(user_id),
                self._model.is_recipient_read == False
                 )
        ).order_by(
            self._model.sender_date
        )
        msgs = await self._session.execute(stmt)

        if msgs:
            return tuple(msgs.scalar().all())
        return ()

        # get_stmt = select(self._model).where(
        #     self._model.id.in_(msgs_ids)
        # )
        # result = await self._session.execute(get_stmt)


    async def send_msg(self, msg: MediatorMessageBase, chat_limit: int=None):
        if chat_limit is not None:
            chat_id = msg.mediator_chat_id
            stmt = select(self._model).where(
                self._model.mediator_chat_id == chat_id
            ).order_by(
                self._model.sender_date
            )
            result = await self._session.execute(stmt)

            chat_msgs = tuple(result.scalars().all())

            if len(chat_msgs) >= chat_limit:
                delete_stmt = delete(self._model).where(
                    self._model.id == chat_msgs[0].id
                )
                await self._session.execute(delete_stmt)

        self._session.add(msg)
        await self._session.commit()

    async def delete_msgs(self, chat_id: str):
        stmt = delete(self._model).where(self._model.mediator_chat_id == chat_id)
        await self._session.execute(stmt)
        await self._session.commit()


class ProductStatisticRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductBase)

