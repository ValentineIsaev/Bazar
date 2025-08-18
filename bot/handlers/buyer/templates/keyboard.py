from aiogram.types import inline_keyboard_markup

from bot.utils.message_utils.keyboard_utils import create_callback, create_callback_inline_keyboard, InlineButtonSetting

START_KEYBOARD = create_callback_inline_keyboard(InlineButtonSetting(text='Купить товар',
                                                                     callback=create_callback('buy_product',
                                                                                              'choice_product',
                                                                                              'start')),
                                                 InlineButtonSetting(text='Моя история',
                                                                     callback='_'),
                                                 InlineButtonSetting(text='Вывести деньги',
                                                                     callback='_'),
                                                 InlineButtonSetting(text='Пополнить счет',
                                                                     callback='_'))
def PRODUCT_ACTIONS() -> inline_keyboard_markup:
    return create_callback_inline_keyboard(InlineButtonSetting(text='Купить товар', callback=create_callback(
    'buy_product',
    'buy_product',
    'choice_product'
)))

UNDO_BUY_PRODUCT = create_callback_inline_keyboard(InlineButtonSetting(text='Отменить',
                                                                       callback=create_callback('buy_product',
                                                                                                'buy_product',
                                                                                                'back')))