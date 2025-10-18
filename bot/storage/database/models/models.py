from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime, ARRAY, String

from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class ProductBase(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int]
    autor_id: Mapped[int]

    name_product: Mapped[str]
    catalog: Mapped[str]
    price: Mapped[float]
    media_path: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    amount: Mapped[int]
    description: Mapped[str]= mapped_column(nullable=True)


class UserBase(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int]
    tg_chat_id: Mapped[int]


class MoneyBalanceBase(Base):
    __tablename__ = 'money_balance'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int]
    money_amount: Mapped[float]


class MediatorChatBase(Base):
    __tablename__ = 'mediator_chats'

    id: Mapped[int] = mapped_column(primary_key=True)

    seller_user_id: Mapped[int]
    buyer_user_id: Mapped[int]
    product_id: Mapped[int]

    mediator_chat_id: Mapped[int]
    chat_name: Mapped[str]


class MediatorMessageBase(Base):
    __tablename__ = 'mediator_messages'

    id: Mapped[int] = mapped_column(primary_key=True)

    mediator_chat_id: Mapped[int]
    sender_id: Mapped[int]

    sender_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    media_path: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)


class RefCatalogBase(Base):
    __tablename__ = 'ref_catalogs'

    id: Mapped[int] = mapped_column(primary_key=True)

    catalog: Mapped[str]
