from aiogram.types import inline_keyboard_markup

from bot.types.utils import CallbackSetting
from bot.utils.message_utils.keyboard_utils import get_callback_inline_keyboard, InlineButtonSetting

START_KEYBOARD = (InlineButtonSetting(text='🏪 Купить товар',
                                      callback=CallbackSetting('buy_product',
                                                               'choice_product',
                                                               'start')),
                  InlineButtonSetting(text='🛒 Корзина',
                                      callback=CallbackSetting('_', '_', '_')))
