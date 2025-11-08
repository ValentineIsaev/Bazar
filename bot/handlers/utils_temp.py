from bot.types.utils import TextTemplate

PRODUCT_TEXT = TextTemplate('Каталог: ?\n\nНазвание товара: ?\n\nОписание: ?\nСтоимость: ?')

INVALID_PRICE = TextTemplate('Вы неправильно ввели значение цены товара: ?\n Попробуйте вновь:')