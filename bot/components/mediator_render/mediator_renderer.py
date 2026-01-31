from abc import abstractmethod
from typing import TypeVar, Generic
from bot.services.mediator_chat import ChatMessage, Chat
from bot.utils.message_utils import get_callback_inline_keyboard
from bot.types.utils import InlineButtonSetting

from bot.types.utils import MessageSetting
from bot.utils.message_utils.config_obj import CallbackSetting

RenderType = TypeVar('RenderType')
class MediatorRenderer(Generic[RenderType]):
    @abstractmethod
    def render_chat_msgs(self, msgs: tuple[ChatMessage, ...]) -> RenderType:
        pass

class MediatorTelegramRenderer(MediatorRenderer[MessageSetting]):
    def render_chat_msgs(self, msgs: tuple[ChatMessage, ...]) -> MessageSetting:
        text = 'Ничего нет.'
        if msgs is not None and len(msgs) > 0:
            text = ' '.join(msg.text for msg in msgs)
        return MessageSetting(text=text, keyboard=get_callback_inline_keyboard(InlineButtonSetting(
            text='Отправить сообщение', callback=CallbackSetting('mediator_chat', 'msgs', 'send'))))