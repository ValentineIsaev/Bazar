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