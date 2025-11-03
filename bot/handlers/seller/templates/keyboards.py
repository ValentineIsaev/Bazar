from bot.utils.message_utils import get_callback_inline_keyboard
from bot.types.utils import InlineButtonSetting, CallbackSetting

MENU_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Добавить товар',
                                                                 callback=CallbackSetting.encode_callback('product',
                                                                                          'add',
                                                                                          'start')),
                                             InlineButtonSetting(text='Удалить товар',
                                                                 callback=CallbackSetting.encode_callback('product',
                                                                                          'delete',
                                                                                          'start')),
                                             InlineButtonSetting(text='Вывести деньги',
                                                                 callback='withdraw_money'))

EDIT_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Имя',
                                                                         callback=CallbackSetting.encode_callback(
                                                                             'product',
                                                                             'edit_product',
                                                                             'name')), InlineButtonSetting(text='Цена',
                                                                                                           callback=CallbackSetting.encode_callback(
                                                                                                               'product',
                                                                                                               'edit_product',
                                                                                                               'price'
                                                                                                           )),
                                                     InlineButtonSetting(text='Описание',
                                                                         callback=CallbackSetting.encode_callback('product',
                                                                                                  'edit_product',
                                                                                                  'description',
                                                                                                  )),
                                                     InlineButtonSetting(text='Каталог',
                                                                         callback=CallbackSetting.encode_callback('product',
                                                                                                  'add',
                                                                                                  'start')),
                                                     InlineButtonSetting(text='Фото',
                                                                         callback=CallbackSetting.encode_callback(
                                                                             'product',
                                                                             'edit_product',
                                                                             'media'
                                                                         )))
ADD_PRODUCT_COMPLETE_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Да',
                                                                                 callback=CallbackSetting.encode_callback(
                                                                                     'product',
                                                                                     'add',
                                                                                     'send_product',
                                                                                 )), InlineButtonSetting(
    text='Нет',
    callback=CallbackSetting.encode_callback(
        'product',
        'edit_product',
        'start'
    )))