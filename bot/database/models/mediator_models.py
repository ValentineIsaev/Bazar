from sqlalchemy.orm import Mapped

from .base import Base

class ChatMediatorBase(Base):
    __tablename__ = 'mediator_chat'

    receiver_id: Mapped[int]
    sender_id: Mapped[int]
    action: Mapped[str]
    msg_text: Mapped[str] | Mapped[None]
    msg_media: Mapped[str] | Mapped[None]