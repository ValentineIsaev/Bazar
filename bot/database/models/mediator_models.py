from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class ChatMediatorBase(Base):
    __tablename__ = 'mediator_chat'

    id: Mapped[int] = mapped_column(primary_key=True)

    receiver_id: Mapped[int]
    receiver_role: Mapped[str]
    sender_id: Mapped[int]
    action: Mapped[str]
    msg_text: Mapped[str | None]
    msg_media: Mapped[str | None]