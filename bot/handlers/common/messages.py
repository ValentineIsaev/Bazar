from bot.utils.message_utils.message_utils import MessageSetting
from bot.configs.constants import UserTypes

START_MESSAGE = MessageSetting(text='Рады видеть Вас на нашей платформе!\n\n'
                                    'Используйте /catalog для перехода к каталогу или /seller для размещения товара')
HELP_MESSAGE = MessageSetting(text='Help message')
DEFAULT_MESSAGES = {
    UserTypes.DEFAULTS: START_MESSAGE,
}
