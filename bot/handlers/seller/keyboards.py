from bot.constants.callback import SELLER_MENU_CALLBACK
from bot.utils.message_utils import get_callback_inline_keyboard
from bot.types.utils import InlineButtonSetting, CallbackSetting

GO_TO_SELLER_MENU_BUTTON = InlineButtonSetting(text='🏠 Главное меню',
                                               callback=SELLER_MENU_CALLBACK)

MENU_KEYBOARD = (InlineButtonSetting(text='📤 Добавить товар',
                                     callback=CallbackSetting('product',
                                                              'add_catalog',
                                                              'start')),
                InlineButtonSetting(text='🔧 Редактировать товар',
                             callback=CallbackSetting('product',
                                                      'choose_product',
                                                      'start_edit')),
                InlineButtonSetting(text='🗑️ Удалить товар',
                             callback=CallbackSetting('product',
                                                      'choose_product',
                                                      'start_delete')))

EDIT_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='🧸 Название',
                                                                         callback=CallbackSetting('product',
                                                                                                  'edit',
                                                                                                  'name')),
                                                     InlineButtonSetting(text='💰 Стоимость',
                                                                        callback=CallbackSetting('product',
                                                                                                'edit',
                                                                                                'price'
                                                                        )),
                                                     InlineButtonSetting(text='📄 Описание',
                                                                         callback=CallbackSetting('product',
                                                                                                  'edit',
                                                                                                  'description',
                                                                                                  )),
                                                     InlineButtonSetting(text='🗂 Каталог',
                                                                         callback=CallbackSetting('product',
                                                                                                  'edit',
                                                                                                  'catalog')),
                                                     InlineButtonSetting(text='📷 Фото',
                                                                         callback=CallbackSetting('product',
                                                                                                  'edit',
                                                                                                  'media'
                                                                         )))
ADD_PRODUCT_COMPLETE_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Сохранить ✅',
                                                                                 callback=CallbackSetting('product',
                                                                                                          'save',
                                                                                                          '_')),
                                                             InlineButtonSetting(text='Редактировать ❌',
                                                                                 callback=CallbackSetting('product',
                                                                                                          'edit',
                                                                                                          'start'
                                                                                 )))

SET_SEARCH_DATA_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='🗂 Каталог',
                                                                            callback=CallbackSetting('seller_product_catalog',
                                                                                                     'filtering',
                                                                                                     'set_catalog_filter')),
                                                        InlineButtonSetting(text='🧸 Название', callback=CallbackSetting('seller_product_catalog',
                                                                                                                         'filtering',
                                                                                                                         'set_name_filter')))


DELETE_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='Да ✅',
                                                                           callback=CallbackSetting('product',
                                                                                                    'delete_product',
                                                                                                    'delete')),
                                                       InlineButtonSetting(text='Нет ❌',
                                                                           callback=CallbackSetting('product',
                                                                                                    'choose_product',
                                                                                                    'start_delete')))
SUCCESSFUL_CREATE_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='📤 Добавить товар',
                                                                                      callback=CallbackSetting('product',
                                                                                                               'add_catalog',
                                                                                                               'start')),
                                                                  GO_TO_SELLER_MENU_BUTTON)
SUCCESSFUL_EDIT_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='🔧 Редактировать еще',
                                                                                    callback=CallbackSetting('product',
                                                                                                             'choose_product',
                                                                                                             'start_edit')),
                                                                GO_TO_SELLER_MENU_BUTTON)

SUCCESSFUL_DELETE_PRODUCT_KEYBOARD = get_callback_inline_keyboard(InlineButtonSetting(text='🗑️ Удалить еще',
                                                                                      callback=CallbackSetting('product',
                                                                                                               'choose_product',
                                                                                                               'start_delete')),
                                                                  InlineButtonSetting(text='📤 Добавить товар',
                                                                                      callback=CallbackSetting('product',
                                                                                                               'add_catalog',
                                                                                                               'start')),
                                                                  GO_TO_SELLER_MENU_BUTTON)