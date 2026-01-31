from .keyboards import ADD_PRODUCT_COMPLETE_KEYBOARD, EDIT_PRODUCT_KEYBOARD, SET_SEARCH_DATA_KEYBOARD, \
    DELETE_PRODUCT_KEYBOARD, SUCCESSFUL_EDIT_PRODUCT_KEYBOARD, SUCCESSFUL_CREATE_PRODUCT_KEYBOARD, \
    SUCCESSFUL_DELETE_PRODUCT_KEYBOARD

from bot.types.managers import InputProductManager
from bot.types.utils import TextTemplate, MessageSetting, ParseModes
from bot.utils.message_utils import get_reply_keyboard

from bot.components.catalog_renderer.templates import ADD_CATALOG_TO_PRODUCT

START_TEXT_MSG = TextTemplate('Ты в меню продавца.\n🗒 Твой профиль:\n'
                              '\n🛠️ Создано товаров:'
                              '\n🛒 Продано товаров: ?'
                              '\nСтатистика ведется за месяц\n'
                              '\n💎 Баланс: ?')

EDIT_PRODUCT_MESSAGE = MessageSetting(text='📝 *Редактирование вашего товара*\n\n'
                                           'Выберите параметр для изменения из списка ниже\\.\n'
                                           'После выбора вы сможете ввести новое значение\.',
                                      keyboard=EDIT_PRODUCT_KEYBOARD,
                                      parse_mode=ParseModes.MARKDOWN_V2)

INPUT_PRODUCT_NAME_MESSAGE = MessageSetting(text='🧸 *Название товара*\n\nНапишите короткое и запоминающиеся'
                                                 ' название для вашего товара\n\n_\\* Содержит не более 50 символов_ ✅'
                                                 '\n_\\* Не содержит в себе специальных символов и эмодзи_✅\n\n'
                                                 '📝 Пример хорошего названия: \n_"Смартфон Xiaomi Redmi Note 12"_',
                                            parse_mode=ParseModes.MARKDOWN_V2)
INPUT_DESCRIPTION_MESSAGE = MessageSetting(text='📄 *Описание товара*\n\nНапишите описание вашего товара\\. Это поможет '
                                                'пользователю лучше понять, подходит ли ваше предложение его требованиям\\. '
                                                'Покупатель всегда может задать вам уточняющий вопрос\\.'
                                                '\n\n_\\* Не содержит в себе специальных символов и эмодзи_ ✅'
                                                '\n_\\* Не более 1000 символов_ ✅',
                                           parse_mode=ParseModes.MARKDOWN_V2)
SELECTED_CATALOG_TEXT = TextTemplate(ADD_CATALOG_TO_PRODUCT + '\n\nВыбранный каталог\\: ?')
PHOTO_INPUT_STOP_TEXT = 'Это все.'
PHOTO_SKIP_INPUT_TEXT = 'Пропустить.'
PROCESS_INPUT_PHOTO_PRODUCT_MESSAGE = MessageSetting(text='Это все?', keyboard=get_reply_keyboard(
    PHOTO_INPUT_STOP_TEXT))
INPUT_PHOTO_PRODUCT_MESSAGE = MessageSetting(text='📷 *Фото товара*\n\nОтправьте внешний вид вашего товара и сделайте ваше '
                                                  'предложение более детальным\\. Вы можете оставить это поле пустым '
                                                  'воспользовавшись кнопкой "пропустить" ниже'
                                                  '\n\n_\\* Поддерживаются только форматы изображений \\*\\.png, '
                                                  '\\*\\.jpeg, \\*\\.jpg, а также \\*\\.gif_ ✅'
                                                  '\n_\\* Максимально возможный размер файла 10 мб_ ✅',
                                             parse_mode=ParseModes.MARKDOWN_V2)
INPUT_PRICE_PRODUCT_MESSAGE = MessageSetting(text='💰 *Стоимость товара*'
                                                  '\n\nУкажите цену на ваш товар, которую считаете приемлемой\\.'
                                                  '\n\n_\\* Цена не может быть равна нулю_ ✅'
                                                  '\n_\\* Валюта цены \\- ₽ \\(рубли\\)_ ✅',
                                             parse_mode=ParseModes.MARKDOWN_V2)


COMPLETE_ADD_PRODUCT_MESSAGE = MessageSetting(text='📋 *Проверьте данные товара*\n\nПеред сохранением убедитесь, что все поля заполнены верно\\. '
                                                   '\n\n*Сохраненный товар возможно редактировать*\\ ',
                                                         keyboard=ADD_PRODUCT_COMPLETE_KEYBOARD,
                                              parse_mode=ParseModes.MARKDOWN_V2)

POST_PROCESSING_TEXT = 'Используйте кнопки ниже или команду /start для навигации'
SUCCESSFUL_CREATE_PRODUCT_MESSAGE = MessageSetting(text='Товар успешно сохранен ✅')
POST_CREATE_PRODUCT_MESSAGE = MessageSetting(text='🎉 *Спасибо за ваш товар!*\n\n'
                                                  'Ваше предложение успешно добавлено в наш каталог и теперь доступно покупателям\\.\n\n'
                                                  +POST_PROCESSING_TEXT,
                                             keyboard=SUCCESSFUL_CREATE_PRODUCT_KEYBOARD,
                                             parse_mode=ParseModes.MARKDOWN_V2)

SUCCESSFUL_EDIT_PRODUCT_MESSAGE = MessageSetting(text='Изменения успешно сохранены ✅')
POST_EDIT_PRODUCT_MESSAGE = MessageSetting(text=POST_PROCESSING_TEXT,
                                           keyboard=SUCCESSFUL_EDIT_PRODUCT_KEYBOARD)

SET_SEARCH_DATA_MESSAGE = MessageSetting('🔍 *Настройка сортировки*\n\n'
                                         'Выберите основное поле для сортировки товаров:',
                                         keyboard=SET_SEARCH_DATA_KEYBOARD,
                                         parse_mode=ParseModes.MARKDOWN_V2)
SET_NAME_SEARCH_PRODUCT_MSG = MessageSetting('Введите полное название продукта или его часть.')

DELETE_PRODUCT_MESSAGE = MessageSetting(text='🗑️ *Удаление товара*'
                                             '\n\nВы уверены, что хотите удалить этот товар из каталога?\n\n'
                                             '‼️ *Внимание, это действие отменить нельзя*', keyboard=DELETE_PRODUCT_KEYBOARD,
                                        parse_mode=ParseModes.MARKDOWN_V2)
SUCCESSFUL_DELETE_PRODUCT = MessageSetting(text='Продукт успешно удален ✅')
POST_DELETE_PRODUCT_MSG = MessageSetting(text=POST_PROCESSING_TEXT,
                                         keyboard=SUCCESSFUL_DELETE_PRODUCT_KEYBOARD)