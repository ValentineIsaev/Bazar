from dataclasses import dataclass

from bot.services.product.messages import INVALID_PRICE_MESSAGE

from bot.utils.cache_utils.operators import CacheMediaOperator
from bot.utils.message_utils.message_utils import MessageSetting


class CatalogMenu:
    def __init__(self, catalogs, page_capacity: int):
        self._page = 0
        self._catalogs = catalogs

        self._page_capacity = page_capacity

    @property
    def is_end_page(self) -> bool:
        return self._page * 2 * self._page_capacity >= len(self._catalogs)-1

    @property
    def is_start_page(self) -> bool:
        return self._page == 0

    def next_page(self):
        if not self.is_end_page:
            self._page += 1

    def back_page(self):
        if self._page > 0:
            self._page -= 1

    def get_catalogs(self) -> tuple:
        start_index = self._page * self._page_capacity
        end_index = min(start_index + self._page_capacity, len(self._catalogs)-1)

        return self._catalogs[start_index:end_index]


@dataclass()
class ValidationResult:
    is_validate: bool
    error_message: MessageSetting | None = None


@dataclass()
class Product:
    name: str | None = None
    price: str | None = None
    catalog: str | None = None
    description: str | None = None
    media: CacheMediaOperator | None = None


class InputProduct(Product):
    def __init__(self):
        super().__init__()

    @property
    def price(self):
        return self._price

    @property
    def media(self):
        return self._media

    @price.setter
    def price(self, price: str) -> ValidationResult:
        try:
            float(price)
            self._price = price
            return ValidationResult(is_validate=True)
        except ValueError:
            return ValidationResult(is_validate=False, error_message=INVALID_PRICE_MESSAGE)

    @media.setter
    def media(self, media: CacheMediaOperator) -> ValidationResult:
        self._media = media
        return ValidationResult(is_validate=True)

    def add_value(self, field_name: str, value) -> None | MessageSetting:
        """
        Function for update and validate data in product form
        :param field_name: name property of product form class
        :param value: new value product class
        :return:
        None - validate is successfully or MessageSetting - validation error
        """

        prop = getattr(type(self), field_name)
        if isinstance(prop, property):
            result: ValidationResult = prop.fset(self, value)
            if not result.is_validate:
                return result.error_message
        else:
            setattr(self, field_name, value)
        return None

print(InputProduct().add_value('price', 56))