from .keyboards import KEYBOARD_SEND_ANSWER

from bot.services.mediator_chat.constants import Errors
from bot.types.utils import MessageSetting, ParseModes

INPUT_MEDIATOR_MSG = MessageSetting(text='*Отправка анонимного сообщения* 💬\n\nВведите текст сообщения или '
                                         'пришлите фотографию/видео\n\n'
                                         '*Можно прислать либо медиа, либо текст. Ваша личность будет скрыта от получателя*:',
                                    parse_mode=ParseModes.MARKDOWN_V2)
SUCCESSFUL_SEND_ANSWER_MSG = MessageSetting(text='Ваше сообщение успешно доставлено! 🕊')
POST_SEND_MSG = MessageSetting(text='Используйте кнопки ниже или команду /start для навигации',
                               keyboard=KEYBOARD_SEND_ANSWER)

ERROR_ENTERS_REPLY_MSGS = {
    Errors.SHORT_LEN: MessageSetting(text='Сообщение слишком коротко, попробуйте еще раз!')
}