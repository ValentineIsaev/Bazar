from bot.types.utils import InputMedia
from dataclasses import dataclass

from .dto import Product, ProductInputField
from .constants import ValidateErrors


@dataclass
class ValidationResult:
    is_validate: bool
    error: ValidateErrors | None = None


class InputProductService:
    def __init__(self, product: Product=None):
        self._product = Product() if product is None else product

        self._VALIDATION_FUNCS = {
            'price': self._validate_price,
            'media': self._validate_media
        }

    @property
    def product(self):
        return self._product

    def _validate_price(self, price: str | int) -> ValidationResult:
        try:
            float(price)
            return ValidationResult(is_validate=True)
        except ValueError:
            return ValidationResult(is_validate=False, error=ValidateErrors.INVALID_PRICE)

    def _validate_media(self, media: InputMedia) -> ValidationResult:
        return ValidationResult(is_validate=True)

    def add_value(self, field_name: ProductInputField, value) -> None | str:
        """
        Function for update and validate data in product form
        :param field_name: name property of product form class
        :param value: new value product class
        :return:
        None - validate is successfully or MessageSetting - validation error
        """

        if not hasattr(self._product, field_name):
            raise ValueError(f'{field_name} is not exist!')
        if field_name in self._VALIDATION_FUNCS:
            result: ValidationResult = self._VALIDATION_FUNCS.get(field_name)(value)
            if not result.is_validate:
                return result.error
        setattr(self._product, field_name, value)
        return None


# class CatalogMenuService:
#     def __init__(self, catalogs: tuple, page_capacity: int):
#         self._page = 0
#         self._catalogs = catalogs
#
#         self._page_capacity = page_capacity
#
#     @property
#     def is_end_page(self) -> bool:
#         return (self._page+1) * self._page_capacity >= len(self._catalogs)
#
#     @property
#     def is_start_page(self) -> bool:
#         return self._page == 0
#
#     def next_page(self):
#         if not self.is_end_page:
#             self._page += 1
#
#     def back_page(self):
#         if self._page > 0:
#             self._page -= 1
#
#     def get_catalogs(self) -> tuple:
#         start_index = self._page * self._page_capacity
#         end_index = min(start_index + self._page_capacity, len(self._catalogs))
#
#         return self._catalogs[start_index:end_index]


# class ProductService:
#     MAX_VISIBLE_CATALOGS = 20
#
#     @staticmethod
#     def get_product_catalog() -> CatalogMenuService:
#         return CatalogMenuService(
#             ("Электроника",
#             "Одежда",
#             "Обувь",
#             "Дом и сад",
#             "Красота и уход",
#             "Спорт и фитнес",
#             "Автотовары",
#             "Книги",
#             "Игрушки и игры",
#             "Зоотовары",
#             "Бытовая техника",
#             "Строительство и ремонт",
#             "Продукты питания",
#             "Товары для офиса",
#             "Аксессуары",
#             "Туризм и отдых",
#             "Детские товары",
#             "Цифровые товары",
#             "Антиквариат и коллекции",
#             "Ювелирные изделия",
#             "Табачные изделия",
#             'Продуктовые изделия'
#         ),
#             ProductService.MAX_VISIBLE_CATALOGS
#             )
#
#     @staticmethod
#     def get_products(catalog: str) -> CatalogMenuService:
#         return CatalogMenuService(
#             (Product(name='Parliament', price='300', description='Дорогие приятные крепкие сигареты',
#                     media=MediaSetting(type_media=TypesMedia.TYPE_PHOTO,
#                                        path=Path('/home/valentine/PythonProject/Bazar/bot/uploads/1.jpeg'))),
#                     Product(name='Philipmorris', price='200', description='Вкусные сигареты с кнопкой'),
#                     Product(name='Camel', price='222', description='Старый добрый верблюд',
#                             media=MediaSetting(type_media=TypesMedia.TYPE_PHOTO,
#                                                path=Path('/home/valentine/PythonProject/Bazar/bot/uploads/2.jpeg'))
#                             ),
#             Product(name='Chapman', price='300', description='Роллсройс в мире сигарет')
#         ),
#         page_capacity=1)
#
#     @staticmethod
#     def send_product(product: Product) -> None:
#         pass
#
#     @staticmethod
#     def get_product(product_id: int) -> Product:
#         pass
