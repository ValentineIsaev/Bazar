from bot.utils.message_utils.keyboard_utils import (get_callback_inline_keyboard, InlineButtonSetting,
                                                    create_callback)

MENU_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Добавить товар',
                                                                 callback=create_callback('product',
                                                                                          'add',
                                                                                          'start')),
                                             InlineButtonSetting(text='Удалить товар',
                                                                 callback=create_callback('product',
                                                                                          'delete',
                                                                                          'start')),
                                             InlineButtonSetting(text='Вывести деньги',
                                                                 callback='withdraw_money'))

EDIT_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Имя',
                                                                         callback=create_callback(
                                                                             'product',
                                                                             'edit_product',
                                                                             'name')), InlineButtonSetting(text='Цена',
                                                                                                           callback=create_callback(
                                                                                                               'product',
                                                                                                               'edit_product',
                                                                                                               'price'
                                                                                                           )),
                                                     InlineButtonSetting(text='Описание',
                                                                         callback=create_callback('product',
                                                                                                  'edit_product',
                                                                                                  'description',
                                                                                                  )),
                                                     InlineButtonSetting(text='Каталог',
                                                                         callback=create_callback('product',
                                                                                                  'add',
                                                                                                  'start')),
                                                     InlineButtonSetting(text='Фото',
                                                                         callback=create_callback(
                                                                             'product',
                                                                             'edit_product',
                                                                             'media'
                                                                         )))
ADD_PRODUCT_COMPLETE_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Да',
                                                                                 callback=create_callback(
                                                                                     'product',
                                                                                     'add',
                                                                                     'send_product',
                                                                                 )), InlineButtonSetting(
    text='Нет',
    callback=create_callback(
        'product',
        'edit_product',
        'start'
    )))