from pathlib import Path

from bot.managers.session_manager.session import SessionManager
from bot.database.models.mediator_models import ChatMediatorBase

from bot.database.repository import MediatorRepository

from .dto import ChatMessage, Chat

from .constants import *


class BuyerChatService:
    def __init__(self, repository: MediatorRepository):
        self._repository = repository

    async def send_message(self, send_msg: ChatMessage, chat_name: str, chat_id: int) -> None:
        if isinstance(send_msg.media, Path):
            send_msg.media = str(send_msg.media)
        new_message = ChatMediatorBase(receiver_id=send_msg.recipients_id, receiver_role=send_msg.recipients_role,
                                       sender_id=send_msg.senders_id,
                                       sender_role=send_msg.senders_role,
                                       action=ACTION_SEND_MESSAGE, msg_text=send_msg.text,
                                       msg_media=send_msg.media,
                                       chat_name=chat_name,
                                       chat_id=chat_id)

        await self._repository.update(new_message)

    async def stop_chat(self, user_id: int):
        pass

    async def get_updates(self, role_user: str, user_id: int) -> tuple[Chat, ...]:
        chats: tuple[tuple[ChatMediatorBase], ...] = await self._repository.get_chats(role_user, user_id)

        result = []
        for chat in chats:
            is_stop = True if chat[-1].action == ACTION_BAN_USER else False

            result.append(Chat(chat[0].chat_id,
                                chat[0].receiver_id,
                                chat[0].receiver_role,
                                chat[0].sender_id,
                                chat[0].sender_role,
                                chat[0].chat_name,
                                is_stop))

        return tuple(result)


    async def get_chat(self, chat_id: int) -> tuple[ChatMessage, ...]:
        chat = await self._repository.get_chat(chat_id)

        return tuple(ChatMessage(msg.sender_id, msg.sender_role, msg.receiver_id,
                                 msg.receiver_role, msg.msg_text,
                                 (Path(msg.msg_media) if msg.msg_media else None)) for msg in chat)
