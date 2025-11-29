from aiogram.types import inline_keyboard_markup

from bot.types.utils import CallbackSetting
from bot.utils.message_utils.keyboard_utils import get_callback_inline_keyboard, InlineButtonSetting

START_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Купить товар',
                                                                  callback=CallbackSetting.encode_callback('buy_product',
                                                                                           'choice_product',
                                                                                           'start')))

BUY_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Оплатить',
                                                                        callback=CallbackSetting.encode_callback('buy_product',
                                                                                                                 'buy',
                                                                                                                 'buy')),
                                                    InlineButtonSetting(text='Обратно',
                                                                        callback=CallbackSetting.encode_callback('buy_product',
                                                                                                                 'buy',
                                                                                                                 'back')),
                                                    InlineButtonSetting(text='Задать вопрос',
                                                                        callback=CallbackSetting.encode_callback('_', '_', '_')))