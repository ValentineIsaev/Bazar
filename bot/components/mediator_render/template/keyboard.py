from bot.types.utils import CallbackSetting, InlineButtonSetting

GO_TO_PRODUCT_TEXT = 'Перейти к товару ↗️'
SEND_MSG_BUTTON = InlineButtonSetting(text='Отправить сообщение 📩',
                        callback=CallbackSetting('mediator_chat', 'msgs', 'send'))
UPDATE_BUTTON = InlineButtonSetting(text='Обновить 🔄',
                        callback=CallbackSetting('mediator_chat', 'msgs', 'get_all'))
DELETE_BUTTON = InlineButtonSetting(text='Удалить чат 🗑',
                        callback=CallbackSetting('mediator_chat', 'chat', 'delete-open_chat'))

BACK_KEYBOARD = InlineButtonSetting(text='Обратно ↩',
                                    callback=CallbackSetting('mediator_chat',
                                                             'chat',
                                                             'get_chats'))
