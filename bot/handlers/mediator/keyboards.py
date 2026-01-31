from bot.types.utils import CallbackSetting, InlineButtonSetting
from bot.utils.message_utils import get_callback_inline_keyboard

KEYBOARD_SEND_ANSWER = get_callback_inline_keyboard(InlineButtonSetting(text='Перейти в чат 💬',
                                                                        callback=CallbackSetting('mediator_chat',
                                                                                                 'msgs',
                                                                                                 'get_all')),
                                                    InlineButtonSetting(text='Вернуться к товару ↩',
                                                                        callback=CallbackSetting('buy_product',
                                                                                                 'buy',
                                                                                                 'back_product')))