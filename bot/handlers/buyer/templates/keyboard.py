from aiogram.types import inline_keyboard_markup

from bot.utils.message_utils.keyboard_utils import create_callback, get_callback_inline_keyboard, InlineButtonSetting

START_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Купить товар',
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
    return get_callback_inline_keyboard(InlineButtonSetting(text='Купить товар', callback=create_callback(
        'buy_product',
        'buy_product',
        'choice_product')), InlineButtonSetting(text='Задать вопрос по товару', callback=create_callback(
        'buy_product',
        'info_product',
        'send_answer'
    )))

UNDO_BUY_PRODUCT = get_callback_inline_keyboard(InlineButtonSetting(text='Отменить',
                                                                    callback=create_callback('buy_product',
                                                                                             'buy_product',
                                                                                             'back')))