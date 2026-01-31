from bot.types.utils import InlineButtonSetting, CallbackSetting

from bot.utils.message_utils import get_callback_inline_keyboard

BUY_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Оплатить 💰',
                                                                        callback=CallbackSetting('buy_product',
                                                                                                 'buy',
                                                                                                 'buy')),
                                                    InlineButtonSetting(text='Обратно ↩️',
                                                                        callback=CallbackSetting('buy_product',
                                                                                                 'buy',
                                                                                                 'back')),
                                                    InlineButtonSetting(text='Задать вопрос 💬',
                                                                        callback=CallbackSetting('mediator_chat',
                                                                                                 'send_answer',
                                                                                                 ' '))
                                                    )