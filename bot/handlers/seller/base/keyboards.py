from bot.utils.keyboard_utils import create_callback_inline_keyboard, InlineButtonSetting, create_callback

MENU_KEYBOARD = create_callback_inline_keyboard(InlineButtonSetting(text='Добавить товар',
                                                                    callback=create_callback('product',
                                                                                             'add',
                                                                                             'start')),
                                                InlineButtonSetting(text='Удалить товар',
                                                                    callback=create_callback('product',
                                                                                             'delete',
                                                                                             'start')),
                                                InlineButtonSetting(text='Вывести деньги',
                                                                    callback='withdraw_money'))