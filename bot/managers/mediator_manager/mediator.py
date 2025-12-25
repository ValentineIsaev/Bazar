from typing import Generic

from sqlalchemy.ext.asyncio import AsyncSession

from bot.storage.postgres.repository import ChatsMediatorRepository, MessagesMediatorRepository
from bot.storage.postgres.repository import MediatorChatBase, MediatorMessageBase
from bot.components.mediator_render import MediatorRenderer, RenderType

from bot.services.mediator_chat import MediatorService

from bot.services.mediator_chat import Chat, ChatMessage

class MediatorManager(Generic[RenderType]):
    def __init__(self, session: AsyncSession, renderer: MediatorRenderer[RenderType],
                 mediator_service: MediatorService):
        self._chat_repo = ChatsMediatorRepository(session)
        self._msg_repo = MessagesMediatorRepository(session)

        self._renderer = renderer
        self._service = mediator_service

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
                                         media_path=[msg.media.path] if msg.media is not None else None,
                                         text=msg.text) for msg in msgs)

    def __msgs_model_to_dto(self, *msgs_model: MediatorMessageBase) -> tuple[ChatMessage]:
        pass

    async def get_chats(self, user_id: int, user_role: str) -> tuple[Chat, ...]:
        chats = await self._chat_repo.get_chats(user_id, user_role)
        return self.__chat_model_to_dto(*chats)

    async def _get_msgs(self, chat_id: str, user_id: int) -> tuple[ChatMessage, ...]:
        msgs = await self._msg_repo.get_chat_msgs(chat_id)
        return self._service.processing_chat_msgs(msgs, user_id)

    async def get_render_msgs(self, chat_id: str, user_id: int) -> RenderType:
        msgs = await self._get_msgs(chat_id, user_id)
        return self._renderer.render_chat_msgs(msgs)

    async def delete_chat(self, chat_id: str):
        await self._chat_repo.delete_chat(chat_id)
        await self._msg_repo.delete_msgs(chat_id)

    async def start_chat(self, seller_id: int,
                         buyer_id: int,
                         product_id: int,
                         product_name: str) -> Chat:
        chat_data = self._service.start_chat(seller_id, buyer_id, product_id, product_name)
        new_chat = self.__chat_dict_to_model(chat_data)[0]
        chat_model = await self._chat_repo.start_chat(new_chat)

        return self.__chat_model_to_dto(chat_model)[0]

    async def send_msg(self, msg: ChatMessage) -> str:
        result_msg = self._service.processing_send_msg(msg)
        if not result_msg.is_error:
            msg_base = self.__msgs_dto_to_model(msg)[0]
            await self._msg_repo.send_msg(msg_base)
            return ''
        return result_msg.error
