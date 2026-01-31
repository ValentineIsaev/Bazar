from .base import ErrorRenderer, Error, RenderType

from bot.types.utils import MessageSetting, TextTemplate
from bot.services.product.services import ValidateErrors
from bot.managers.product_managers import InputProductManager

class ProductErrorRenderer(ErrorRenderer[MessageSetting, ValidateErrors]):
    INVALID_PRICE = TextTemplate('Вы неправильно ввели значение цены товара: ?\n Попробуйте вновь:')

    INVALIDATE_MSGS = {
        InputProductManager.VALIDATE_ERRORS.INVALID_PRICE: INVALID_PRICE
    }

    def render_error(self, error: ValidateErrors, **kwargs) -> MessageSetting:
        value = kwargs['value']
        return MessageSetting(text=self.INVALIDATE_MSGS.get(error).insert((value,)))