from bot.types.utils import MessageSetting
from bot.services.mediator_chat.constants import Errors
INPUT_MEDIATOR_MSG = MessageSetting(text='Введите текст сообщения или пришлите фотографию/видео (можно одну фотографию в одно сообщение)')

ERROR_ENTERS_REPLY_MSGS = {
    Errors.SHORT_LEN: MessageSetting(text='Сообщение слишком коротко, попробуйте еще раз!')
}