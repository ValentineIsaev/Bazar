from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class ChatMediatorBase(Base):
    __tablename__ = 'mediator_chat'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]

    receiver_id: Mapped[int]
    receiver_role: Mapped[str]

    sender_id: Mapped[int]
    sender_role: Mapped[str]

    chat_name: Mapped[str]
    action: Mapped[str]

    msg_text: Mapped[str | None]
    msg_media: Mapped[str | None]

    def __repr__(self):
        return (f'ChatMediatorBase(id={self.id}, receiver_id={self.receiver_id}, receiver_role={self.receiver_role},'
                f'sender_id={self.sender_id}, action={self.action}, msg_text={self.msg_text}, msg_media={self.msg_media},'
                f'chat_name={self.chat_name})')