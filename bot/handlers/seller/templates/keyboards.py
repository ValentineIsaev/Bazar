from bot.utils.message_utils import get_callback_inline_keyboard
from bot.types.utils import InlineButtonSetting, CallbackSetting

MENU_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Добавить товар',
                                                                 callback=CallbackSetting.encode_callback('product',
                                                                                          'add_catalog',
                                                                                          'start')),
                                             InlineButtonSetting(text='Редактировать товар',
                                                                 callback=CallbackSetting.encode_callback('product',
                                                                                                          'choose_product',
                                                                                                          'start_edit')),
                                             InlineButtonSetting(text='Удалить товар',
                                                                 callback=CallbackSetting.encode_callback('product',
                                                                                          'choose_product',
                                                                                          'start_delete')),
                                             InlineButtonSetting(text='M-chat',
                                                                 callback=CallbackSetting.encode_callback(
                                                                     'mediator_chat',
                                                                     'chat',
                                                                     'get_chats')))

EDIT_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Имя',
                                                                         callback=CallbackSetting.encode_callback(
                                                                             'product',
                                                                             'edit',
                                                                             'name')), InlineButtonSetting(text='Цена',
                                                                                                           callback=CallbackSetting.encode_callback(
                                                                                                               'product',
                                                                                                               'edit',
                                                                                                               'price'
                                                                                                           )),
                                                     InlineButtonSetting(text='Описание',
                                                                         callback=CallbackSetting.encode_callback('product',
                                                                                                  'edit',
                                                                                                  'description',
                                                                                                  )),
                                                     InlineButtonSetting(text='Каталог',
                                                                         callback=CallbackSetting.encode_callback('product',
                                                                                                  'edit',
                                                                                                  'catalog')),
                                                     InlineButtonSetting(text='Фото',
                                                                         callback=CallbackSetting.encode_callback(
                                                                             'product',
                                                                             'edit',
                                                                             'media'
                                                                         )))
ADD_PRODUCT_COMPLETE_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Да',
                                                                                 callback=CallbackSetting.encode_callback(
                                                                                     'product',
                                                                                     'save', '_')), InlineButtonSetting(
    text='Нет',
    callback=CallbackSetting.encode_callback(
        'product',
        'edit',
        'start'
    )))

SET_SEARCH_DATA_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Каталог', callback=CallbackSetting.encode_callback('product',
                                                                                                                                     'choose_product',
                                                                                                                                     'start_set_catalog')))

DELETE_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Да', callback=CallbackSetting.encode_callback('product', 'delete_product', 'delete')),
                                                       InlineButtonSetting(text='Нет', callback=CallbackSetting.encode_callback('product', 'choose_product', 'start_delete')))