from bot.handlers.seller.templates.keyboards import ADD_PRODUCT_COMPLETE_KEYBOARD, EDIT_PRODUCT_KEYBOARD
from bot.utils.message_utils.message_setting_classes import MessageSetting, TextTemplate
from bot.utils.message_utils.keyboard_utils import create_reply_keyboard

START_MESSAGE = TextTemplate('Привет, ?. Твой профиль: \n\nРейтинг: ?\nДеньги: ?')

EDIT_PRODUCT_MESSAGE = MessageSetting(text='Что вы хотите редактировать?', keyboard=EDIT_PRODUCT_KEYBOARD)

ADD_PRODUCT_FORM_TEXT = TextTemplate('Название: ?\nКаталог: ?\nОписание: ?\n\nЦена: ?')

INPUT_PRODUCT_NAME_MESSAGE = MessageSetting(text='Введите пожайлуйста название вашего товара:')
INPUT_DESCRIPTION_MESSAGE = MessageSetting(text='Введите описание товара, '
                                                'чтобы пользователю было проще ориентироваться')
INPUT_PHOTO_PRODUCT_MESSAGE = MessageSetting(text='Вышлите фото товара')
INPUT_PRICE_PRODUCT_MESSAGE = MessageSetting(text='Укажите цену товара')

PHOTO_INPUT_STOP_TEXT = 'Это все.'
SKIP_INPUT_PHOTO_COMMAND = '/skip'
PROCESS_INPUT_PHOTO_PRODUCT_MESSAGE = MessageSetting(text='Это все?', keyboard=create_reply_keyboard(PHOTO_INPUT_STOP_TEXT))

COMPLETE_ADD_PRODUCT_MESSAGE_WITH_MEDIA = MessageSetting(text='Все верно указано?',
                                                         keyboard=ADD_PRODUCT_COMPLETE_KEYBOARD)
COMPLETE_ADD_PRODUCT_MESSAGE = TextTemplate('?\n\nВсе верно указано')