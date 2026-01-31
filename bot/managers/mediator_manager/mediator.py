from typing import Generic
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from bot.managers.base import StorageManager, storage_field, set_storage_field

from bot.constants.redis_keys import StorageKeys
from bot.constants.user_constants import TypesUser
from bot.services.mediator_chat.dto import ErrorSendMessage

from bot.storage.postgres.repository import ChatsMediatorRepository, MessagesMediatorRepository
from bot.storage.postgres.repository import MediatorChatBase, MediatorMessageBase
from bot.components.mediator_render import MediatorRenderer, RenderType

from bot.services.mediator_chat import MediatorService

from bot.services.mediator_chat import Chat, ChatMessage
from bot.types.storage import LocalObjPath, Storage

class MediatorManager(Generic[RenderType], StorageManager):
    _CHAT_LIMIT_MSGS = 10

    def __init__(self, session: AsyncSession, storage_session: Storage, renderer: MediatorRenderer[RenderType],
                 mediator_service: MediatorService):
        super().__init__(storage_session)

        self._chat_repo = ChatsMediatorRepository(session)
        self._msg_repo = MessagesMediatorRepository(session)

        self._renderer = renderer
        self._service = mediator_service

        self._chat: Chat = None

    def __chat_dict_to_model(self, *chats: dict) -> tuple[MediatorChatBase, ...]:
        return tuple(MediatorChatBase(seller_user_id=str(chat.get('seller_id')),
                                      buyer_user_id=str(chat.get('buyer_id')),
                                      product_id=chat.get('product_id'),
                                      mediator_chat_id=chat.get('chat_id'),
                                      chat_name=chat.get('chat_name')) for chat in chats)

    def __chat_model_to_dto(self, *chat_models: MediatorChatBase) -> tuple[Chat, ...]:
        return tuple(Chat(table_id=chat_model.id,
                   chat_id=chat_model.mediator_chat_id,
                   seller_user_id=int(chat_model.seller_user_id),
                   buyer_user_id=int(chat_model.buyer_user_id),
                   product_id=chat_model.product_id,
                   chat_name=chat_model.chat_name) for chat_model in chat_models)

    def __msgs_dto_to_model(self, *msgs: ChatMessage) -> tuple[MediatorMessageBase, ...]:
        return tuple(MediatorMessageBase(mediator_chat_id=msg.chat_id,
                                         sender_id=str(msg.sender_id),
                                         media_path=[media.path for media in msg.media] if msg.media is not None else None,
                                         text=msg.text) for msg in msgs)

    def __msgs_model_to_dto(self, *msgs_model: MediatorMessageBase) -> tuple[ChatMessage, ...]:
        return tuple(ChatMessage(chat_id=msg.mediator_chat_id,
                                 sender_id=int(msg.sender_id),
                                 text=msg.text,
                                 table_msg_id=msg.id,
                                 date=str(msg.sender_date),
                                 media=tuple(LocalObjPath(Path(path)) for path in msg.media_path)
                                 if msg.media_path is not None else None) for msg in msgs_model)

    async def get_chats(self, user_id: int, user_role: TypesUser) -> tuple[Chat, ...]:
        chats = await self._chat_repo.get_chats(user_id, user_role.value)
        dto_chats = self.__chat_model_to_dto(*chats)

        counts_updates = tuple([await self._msg_repo.get_count_new_msgs(chat.chat_id, user_id) for chat in dto_chats])
        return self._service.processing_chats_list(counts_updates, dto_chats)

    @storage_field('_chat', StorageKeys.MEDIATOR_CHAT)
    async def _get_msgs(self, user_id: int) -> tuple[ChatMessage, ...]:
        msgs = await self._msg_repo.get_chat_msgs(self._chat.chat_id)
        chat_msgs = self.__msgs_model_to_dto(*msgs)
        await self._msg_repo.recipient_msgs(
            [msg.id for msg in msgs if msg.sender_id != user_id and msg.is_recipient_read == False], user_id)
        return self._service.processing_chat_msgs(chat_msgs, user_id)

    @storage_field('_chat', StorageKeys.MEDIATOR_CHAT)
    async def _get_new_msgs(self, user_id: int) -> tuple[ChatMessage, ...]:
        msgs = await self._msg_repo.get_new_msgs(self._chat.chat_id, user_id)
        chat_msgs = self.__msgs_model_to_dto(*msgs)
        await self._msg_repo.recipient_msgs(
            [msg.id for msg in msgs if msg.sender_id != user_id and msg.is_recipient_read == False], user_id)
        return self._service.processing_chat_msgs(chat_msgs, user_id)

    @storage_field('_chat', StorageKeys.MEDIATOR_CHAT)
    async def _render_msgs(self, msgs: tuple[ChatMessage, ...], user_id: int) -> RenderType:
        user_role = TypesUser.BUYER if self._chat.buyer_user_id == user_id else TypesUser.SELLER
        return self._renderer.render_chat_msgs(msgs, self._chat, user_role)

    async def get_render_msgs(self, user_id: int) -> RenderType:
        msgs = await self._get_msgs(user_id)
        return await self._render_msgs(msgs, user_id)

    async def get_render_new_msgs(self, user_id: int) -> RenderType:
        msgs = await self._get_new_msgs(user_id)
        if len(msgs) > 0:
            return await self._render_msgs(msgs, user_id)
        return await self.get_render_msgs(user_id)

    async def get_count_all_new_msgs(self, user_id: int, user_role: TypesUser) -> int:
        chats = await self._chat_repo.get_chats(user_id, user_role.value)
        return sum([await self._msg_repo.get_count_new_msgs(chat.mediator_chat_id, user_id) for chat in chats])

    async def delete_chat(self, chat_id: str):
        await self._chat_repo.delete_chat(chat_id)
        await self._msg_repo.delete_msgs(chat_id)

    async def start_chat(self, seller_id: int,
                         buyer_id: int,
                         product_id: int,
                         product_name: str) -> Chat:
        chat_data = self._service.start_chat(seller_id, buyer_id, product_id, product_name)
        new_chat = self.__chat_dict_to_model(chat_data)[0]
        is_chat_exist, chat_model = await self._chat_repo.is_chat_exist(new_chat)
        print(is_chat_exist)
        if not is_chat_exist:
            chat_model = await self._chat_repo.start_chat(new_chat)

        return self.__chat_model_to_dto(chat_model)[0]

    async def send_msg(self, msg: ChatMessage) -> str:
        result_msg = self._service.processing_send_msg(msg)
        if not result_msg.is_error:
            msg_base = self.__msgs_dto_to_model(msg)[0]
            await self._msg_repo.send_msg(msg_base, chat_limit=self._CHAT_LIMIT_MSGS)
            return ''
        return result_msg.error

    @set_storage_field('_chat', StorageKeys.MEDIATOR_CHAT)
    async def set_chat(self, chat: Chat):
        self._chat = chat
