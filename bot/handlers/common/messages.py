from bot.utils.message_utils import MessageSetting
from bot.configs.constants import UserTypes
from ..buyer.messages import DEFAULT_MESSAGE

START_MESSAGE = MessageSetting(text='Рады видеть Вас на нашей платформе!\n\n'
                                    'Используйте /catalog для перехода к каталогу или /seller для размещения товара')
HELP_MESSAGE = MessageSetting(text='Help message')
DEFAULT_MESSAGES = {
    UserTypes.DEFAULTS: START_MESSAGE,
    UserTypes.BUYER: DEFAULT_MESSAGE
}

HEADER_CATALOG_MENU_TEXT = ('Используйте кнопки для выбора номера нужного каталога, '
                            'а также кнопки вперед и назад для пролистывания.\n\n')
