from aiogram.types import inline_keyboard_markup
from bot.types.utils import InlineButtonSetting, CallbackSetting, TextTemplate
from bot.utils.message_utils import get_callback_inline_keyboard

CATALOG_MENU_NEXT = (InlineButtonSetting(text='Вперед ➡️', callback=CallbackSetting('catalog_menu',
                                                                                    'scroll',
                                                                                    'next')),)
CATALOG_MENU_BACK = (InlineButtonSetting(text='⬅️ Назад', callback=CallbackSetting('catalog_menu',
                                                                                   'scroll',
                                                                                   'back')),)

MEDIATOR_COUNT_BUTTON = TextTemplate('[?] ')

CHOOSE_PRODUCT_KEYBOARD = (InlineButtonSetting(text='🎯 Сортировать', callback=CallbackSetting('seller_product_catalog',
                                                                                               'filtering',
                                                                                               'start')))

UPDATE_MEDIATOR_CHATS_BUTTON = InlineButtonSetting(text='Обновить 🔄', callback=CallbackSetting('mediator_chat', 'chat',
                                                                                               'get_chats'))
