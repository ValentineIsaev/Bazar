from bot.types.utils import TextTemplate
from enum import Enum

ACTION_SEND_MESSAGE = 'send_message'
ACTION_BAN_USER = 'ban_user'

chat_name_prefix = TextTemplate('Обсуждение "?"')

class Errors(Enum):
    SHORT_LEN = 'short len'