from aiogram.types import inline_keyboard_markup
from bot.types.utils import InlineButtonSetting, CallbackSetting
from bot.utils.message_utils import get_callback_inline_keyboard

CATALOG_MENU_NEXT = (InlineButtonSetting(text='Вперед', callback=CallbackSetting.encode_callback('catalog_menu',
                                                                                'scroll',
                                                                                'next')),)
CATALOG_MENU_BACK = (InlineButtonSetting(text='Назад', callback=CallbackSetting.encode_callback('catalog_menu',
                                                                                'scroll',
                                                                                'back')),)

def PRODUCT_ACTIONS() -> inline_keyboard_markup:
    return get_callback_inline_keyboard(InlineButtonSetting(text='Купить товар', callback=CallbackSetting.encode_callback(
        'buy_product',
        'buy_product',
        'choice_product')), InlineButtonSetting(text='Задать вопрос по товару', callback=CallbackSetting.encode_callback(
        'buy_product',
        'info_product',
        'send_answer'
    )))

