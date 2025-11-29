from bot.types.utils import InlineButtonSetting, CallbackSetting
from bot.utils.message_utils import get_callback_inline_keyboard

START_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='M-chat',
                                                                  callback=CallbackSetting.encode_callback('_',
                                                                                                           '_',
                                                                                                           '_')),
                                              InlineButtonSetting(text='Деньги',
                                                                  callback=CallbackSetting.encode_callback('-',
                                                                                                           '-',
                                                                                                           '_')))
