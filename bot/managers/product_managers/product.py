from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.product import InputProductService, Product
from bot.services.catalog_service import CatalogMenuService
from bot.storage.redis import Storage

from bot.constants.redis_keys import UserSessionKeys

from bot.storage.database import BaseRepository, RefCatalogBase
from bot.constants import ServiceConstants

from bot.managers.base import StorageManager
from bot.utils.decorators import require_field


class ProductCategoryCatalogManager:
    def __init__(self, db_session: AsyncSession):
        self._catalog_repo = BaseRepository(db_session, RefCatalogBase)

    async def get_product_catalogs(self) -> CatalogMenuService:
        catalogs_model = await self._catalog_repo.get_all()
        return CatalogMenuService(tuple((int(model.id), model.catalog) for model in catalogs_model),
                                  ServiceConstants.CATALOG_MENU_CAPACITY)


class InputProductManager(ProductCategoryCatalogManager, StorageManager):
    def __init__(self, session_storage: Storage, db_session: AsyncSession):
        ProductCategoryCatalogManager.__init__(self, db_session)
        StorageManager.__init__(self, session_storage)

        self._product: InputProductService | None = None

    async def new(self) -> None:
        """
        The method for creating a service for filling in data about a new product.
        """
        self._product = InputProductService()
        await self._storage.update_data(**{UserSessionKeys.INPUT_PRODUCT_SERVICE: self._product})

    @require_field('_product', UserSessionKeys.INPUT_PRODUCT_SERVICE)
    async def add_value(self, field_name: str, value) -> str | None:
        result = self._product.add_value(field_name, value)
        if result is not None:
            await self._storage.update_data(**{UserSessionKeys.INPUT_PRODUCT_SERVICE: self._product})

        return result

    @require_field('_product', UserSessionKeys.INPUT_PRODUCT_SERVICE)
    async def get_product(self) -> Product | None:
        """Getter a service for filling in data about a new product."""
        return self._product.product

    async def create_product(self):
        pass


class ProductManager(ProductCategoryCatalogManager):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
        self._session = db_session

    def get_product(self):
        pass

    def get_products(self, catalog: str):
        pass

    def create_product(self):
        pass
