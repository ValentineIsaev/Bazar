from bot.handlers.seller.templates.keyboards import ADD_PRODUCT_COMPLETE_KEYBOARD, EDIT_PRODUCT_KEYBOARD
from bot.utils.message_utils.message_utils import MessageSetting, TextTemplate

START_MESSAGE = TextTemplate('Привет, ?. Твой профиль: \n\nРейтинг: ?\nДеньги: ?')

EDIT_PRODUCT_MESSAGE = MessageSetting(text='Что вы хотите редактировать?', keyboard=EDIT_PRODUCT_KEYBOARD)

ADD_PRODUCT_FORM_TEXT = TextTemplate('Название: ?\nКаталог: ?\nОписание: ?\n\nЦена: ?')

INPUT_PRODUCT_NAME_MESSAGE = MessageSetting(text='Введите пожайлуйста название вашего товара:')
INPUT_DESCRIPTION_MESSAGE = MessageSetting(text='Введите описание товара, '
                                                'чтобы пользователю было проще ориентироваться')
INPUT_PHOTO_PRODUCT_MESSAGE = MessageSetting(text='Вышлите фото товара')
INPUT_PRICE_PRODUCT_MESSAGE = MessageSetting(text='Укажите цену товара')

PROCESS_INPUT_PHOTO_PRODUCT_MESSAGE = MessageSetting(text='Это все?')

COMPLETE_ADD_PRODUCT_MESSAGE = MessageSetting(text='Все верно указано?', keyboard=ADD_PRODUCT_COMPLETE_KEYBOARD)