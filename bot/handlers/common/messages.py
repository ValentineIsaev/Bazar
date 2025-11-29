from bot.utils.message_utils.message_utils import MessageSetting
from bot.configs.constants import UserTypes

from .keyboard import START_KEYBOARD

START_MESSAGE = MessageSetting(text='Рады видеть Вас на нашей платформе!\nВ этом меню вы можете воспользоваться M-chat '
                                    'для общения с покупателем/продавцом и пополнить/вывести свой денежный баланс\n\n'
                                    'Используйте /catalog для перехода к каталогу или /seller для размещения товара.',
                               keyboard=START_KEYBOARD)
HELP_MESSAGE = MessageSetting(text='Help message')
DEFAULT_MESSAGES = {
    UserTypes.DEFAULTS: START_MESSAGE,
}
