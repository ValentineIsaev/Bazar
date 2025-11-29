from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from bot.services.product import InputProductService, Product, ProductInputField, ValidateErrors
from bot.services.catalog_service import CatalogMenuService
from bot.storage.redis import Storage

from bot.constants.redis_keys import UserSessionKeys

from bot.storage.postgres import BaseRepository, RefCatalogBase
from bot.constants import ServiceConstants

from bot.managers.base import StorageManager
from bot.utils.decorators import require_field

from bot.types.storage import LocalObjPath


class ProductCategoryCatalogManager:
    def __init__(self, db_session: AsyncSession):
        self._catalog_repo = BaseRepository(db_session, RefCatalogBase)

    async def get_category_products(self) -> CatalogMenuService:
        catalogs_model = await self._catalog_repo.get_all()
        return CatalogMenuService(tuple((int(model.id), model.catalog) for model in catalogs_model),
                                  ServiceConstants.CATALOG_MENU_CAPACITY)


class InputProductManager(ProductCategoryCatalogManager, StorageManager):
    PRODUCT_INPUT_FIELD = ProductInputField
    VALIDATE_ERRORS = ValidateErrors

    def __init__(self, session_storage: Storage, db_session: AsyncSession):
        ProductCategoryCatalogManager.__init__(self, db_session)
        StorageManager.__init__(self, session_storage)

        self._product: InputProductService | None = None

    async def set_product(self, product: Product) -> None:
        self._product = InputProductService(product)

        await self._storage.update_value(UserSessionKeys.INPUT_PRODUCT_SERVICE, self._product)

    async def new(self) -> None:
        """
        The method for creating a service for filling in data about a new product.
        """
        self._product = InputProductService()
        await self._storage.update_data(**{UserSessionKeys.INPUT_PRODUCT_SERVICE: self._product})

    @require_field('_product', UserSessionKeys.INPUT_PRODUCT_SERVICE)
    async def add_value(self, field_name: PRODUCT_INPUT_FIELD, value) -> ValidateErrors | None:
        result = self._product.add_value(field_name, value)
        if result is not None:
            await self._storage.update_data(**{UserSessionKeys.INPUT_PRODUCT_SERVICE: self._product})

        return result

    @require_field('_product', UserSessionKeys.INPUT_PRODUCT_SERVICE)
    async def get_product(self) -> Product | None:
        """Getter a service for filling in data about a new product."""
        return self._product.product


class ProductManager(ProductCategoryCatalogManager):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
        self._session = db_session

    def get_products_by_catalog(self, catalog: str) -> tuple[Product, ...]:
        return (Product(1, 1, 1, 'Сигарета', 'Табачные изделия', 255,
                        media_path=(LocalObjPath(path=Path('/home/valentine/PythonProject/Bazar/Storage/Perm/AgACAgIAAxkBAAIRnGkPfH5oLLa1BSDQe2FR2tv9zJPKAALUD2sbJo94SDzCoBtSXXwWAQADAgADeQADNgQ.png')),)),
                Product(2, 2, 2, 'Стиральная машина', 'Хозяйственные товары', 10_000),
                Product(3, 3, 3, 'Мусор', 'Хозяйственные товары', price=0, description='Отдам бесплатно!'))

    def get_products_by_user(self, user_id: int) -> tuple[Product, ...]:
        return (Product(1, 1, 1, 'Сигарета', 'Табачные изделия', 225, ),)

    def buy_product(self, product_id: int, user_id: int):
        pass

    async def create_product(self, product: Product):
        pass

    async def delete_product(self, product_id: int) -> None:
        pass
