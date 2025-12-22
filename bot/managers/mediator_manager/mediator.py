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

    def __chat_dict_to_model(self, *chat: dict) -> tuple[MediatorChatBase, ...]:
        pass

    def __chat_model_to_dto(self, *chat_model: MediatorChatBase) -> tuple[Chat, ...]:
        pass

    def __msgs_dto_to_model(self, *msgs: ChatMessage) -> tuple[MediatorMessageBase, ...]:
        pass

    def __msgs_model_to_dto(self, *msgs_model: MediatorMessageBase) -> tuple[ChatMessage]:
        pass

    async def _get_chats(self, user_id: int, user_role: str) -> tuple[Chat, ...]:
        chats = await self._chat_repo.get_chats(user_id, user_role)
        return self.__chat_model_to_dto(*chats)

    async def get_render_chats(self, user_id, user_role: str) -> RenderType:
        chats = await self._get_chats(user_id, user_role)
        self._renderer.render_chat_list(chats)


    async def _get_msgs(self, chat_id: int, user_id: int) -> tuple[ChatMessage, ...]:
        msgs = await self._msg_repo.get_chat_msgs(chat_id)
        return self._service.processing_chat_msgs(msgs, user_id)

    async def get_render_msgs(self, chat_id: int, user_id: int) -> RenderType:
        msgs = await self._get_msgs(chat_id, user_id)
        return self._renderer.render_chat_msgs(msgs)

    async def delete_chat(self, chat_id: int):
        await self._chat_repo.delete_chat(chat_id)
        await self._msg_repo.delete_msgs(chat_id)

    async def start_chat(self, seller_id: int,
                         buyer_id: int,
                         product_id: int,
                         product_name: str) -> Chat:
        chat_data = self._service.start_chat(seller_id, buyer_id, product_id, product_name)
        new_chat = self.__chat_dict_to_model(chat_data)
        chat_model = await self._chat_repo.start_chat(new_chat)

        return self.__chat_model_to_dto(chat_model[0])[0]

    async def send_msg(self, msg: ChatMessage) -> str:
        result_msg = self._service.processing_send_msg(msg)
        if not result_msg.is_error:
            msg_base = self.__msgs_dto_to_model(msg)[0]
            await self._msg_repo.send_msg(msg_base)
            return ''
        return result_msg.error
