from aiogram.types import inline_keyboard_markup
from bot.utils.message_utils.keyboard_utils import InlineButtonSetting, create_callback,create_callback_inline_keyboard

CATALOG_MENU_NEXT = (InlineButtonSetting(text='Вперед', callback=create_callback('catalog_menu',
                                                                                'scroll',
                                                                                'next')),)
CATALOG_MENU_BACK = (InlineButtonSetting(text='Назад', callback=create_callback('catalog_menu',
                                                                                'scroll',
                                                                                'back')),)

def PRODUCT_ACTIONS() -> inline_keyboard_markup:
    return create_callback_inline_keyboard(InlineButtonSetting(text='Купить товар', callback=create_callback(
    'buy_product',
    'buy_product',
    'choice_product')), InlineButtonSetting(text='Задать вопрос по товару', callback=create_callback(
        'buy_product',
        'info_product',
        'send_answer'
    )))

