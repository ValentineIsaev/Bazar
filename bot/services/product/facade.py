from typing import Callable

from .validation_input_product import ValidationResult
from .models import Product

from bot.utils.message_utils.message_utils import MessageSetting

class AddProductOperator:
    def __init__(self):
        self._product = Product()

    def add_value(self, field_name: str, value, validate_func: Callable=None) -> None | MessageSetting:
        """
        Function for update and validate data in product form
        :param field_name: name property of product form class
        :param value: new value product class
        :param validate_func: function validating the send data
        :return:
        None - validate is successfully or MessageSetting - validation error
        """

        if validate_func is not None:
            validate_result: ValidationResult = validate_func(value)
            if not validate_result.is_validate:
                return validate_result.error_message

        setattr(self._product, field_name, value)

    @property
    def product(self):
        return self._product
