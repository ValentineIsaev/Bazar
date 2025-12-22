from abc import abstractmethod
from typing import TypeVar, Generic
from bot.services.mediator_chat import ChatMessage, Chat

from bot.types.utils import MessageSetting

RenderType = TypeVar('RenderType')
class MediatorRenderer(Generic[RenderType]):
    @abstractmethod
    def render_input_new_msg(self) -> RenderType:
        pass

    @abstractmethod
    def render_chat_list(self, chats: tuple[Chat, ...]) -> RenderType:
        pass

    @abstractmethod
    def render_chat_msgs(self, msgs: tuple[ChatMessage, ...]) -> RenderType:
        pass

class MediatorTelegramRenderer(MediatorRenderer[MessageSetting]):
    def render_input_new_msg(self) -> RenderType:
        pass

    def render_chat_list(self, chats: tuple[Chat, ...]) -> RenderType:
        pass

    def render_chat_msgs(self, msgs: tuple[ChatMessage, ...]) -> RenderType:
        pass