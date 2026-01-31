from abc import abstractmethod
from typing import TypeVar, Generic

from .template.messages import *
from .template.keyboard import DELETE_BUTTON, GO_TO_PRODUCT_TEXT, BACK_KEYBOARD, SEND_MSG_BUTTON, UPDATE_BUTTON

from bot.constants.user_constants import TypesUser

from bot.services.mediator_chat import ChatMessage, Chat
from bot.utils.message_utils import get_callback_inline_keyboard
from bot.types.utils import InlineButtonSetting

from bot.types.utils import MessageSetting, ParseModes, InlineButtonSetting, CallbackSetting

RenderType = TypeVar('RenderType')
class MediatorRenderer(Generic[RenderType]):
    @abstractmethod
    def render_chat_msgs(self, msgs: tuple[ChatMessage, ...], chat_dto: Chat, user_role: TypesUser) -> RenderType:
        pass

class MediatorTelegramRenderer(MediatorRenderer[MessageSetting]):
    def render_chat_msgs(self, msgs: tuple[ChatMessage, ...], chat_data: Chat, user_role: TypesUser) -> MessageSetting:
        text = CHAT_HEAD.insert((MessageSetting.escape_markdown(chat_data.chat_name),))
        for msg in msgs:text += MSG_FORM.insert((ROLE_NAMES.get('SELF') if msg.is_self else ROLE_NAMES.get(user_role),
                                          MessageSetting.escape_markdown(msg.text),
                                          MessageSetting.escape_markdown(msg.date)))

        keyboard = get_callback_inline_keyboard(SEND_MSG_BUTTON,
                                                InlineButtonSetting(text=GO_TO_PRODUCT_TEXT,
                                                                    callback=CallbackSetting('buy_product',
                                                                                             'buy',
                                                                                             f'start_by-{chat_data.product_id}')),
                                                UPDATE_BUTTON, DELETE_BUTTON, BACK_KEYBOARD)

        return MessageSetting(text=text, parse_mode=ParseModes.MARKDOWN_V2,
                              keyboard=keyboard)