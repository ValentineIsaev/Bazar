from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
import time

from bot.services.product import InputProductService, Product, ProductInputField, ValidateErrors
from bot.services.catalog_service import CatalogMenuService
from bot.storage.redis import Storage

from bot.constants.redis_keys import UserSessionKeys

from bot.storage.postgres import BaseRepository, RefCatalogBase, ProductsRepository, ProductBase
from bot.constants import ServiceConstants

from bot.managers.base import StorageManager, storage_field

from bot.types.storage import LocalObjPath


class ProductCategoryManager:
    def __init__(self, db_session: AsyncSession):
        self._catalog_repo = BaseRepository(db_session, RefCatalogBase)

    async def get_category_products(self) -> CatalogMenuService:
        catalogs_model = await self._catalog_repo.get_all()
        return CatalogMenuService(tuple((int(model.id), model.catalog) for model in catalogs_model),
                                  ServiceConstants.CATALOG_MENU_CAPACITY)


class InputProductManager(StorageManager):
    PRODUCT_INPUT_FIELD = ProductInputField
    VALIDATE_ERRORS = ValidateErrors

    def __init__(self, session_storage: Storage):
        super().__init__(session_storage)
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

    @storage_field('_product', UserSessionKeys.INPUT_PRODUCT_SERVICE)
    async def add_value(self, field_name: PRODUCT_INPUT_FIELD, value) -> ValidateErrors | None:
        result = self._product.add_value(field_name, value)
        if result is not None:
            await self._storage.update_data(**{UserSessionKeys.INPUT_PRODUCT_SERVICE: self._product})

        return result

    @storage_field('_product', UserSessionKeys.INPUT_PRODUCT_SERVICE)
    async def get_product(self) -> Product | None:
        """Getter a service for filling in data about a new product."""
        return self._product.product


class ProductManager:
    def __init__(self, db_session: AsyncSession):
        self._product_repo = ProductsRepository(db_session)

    def __model_to_dto(self, *models: ProductBase) -> tuple[Product, ...]:
        return tuple(Product(
            table_id=model.id,
            product_id=model.product_id,
            autor_id=int(model.autor_id),
            name_product=model.name_product,
            catalog=model.catalog,
            price=model.price,
            media_path=tuple(LocalObjPath(Path(path)) for path in model.media_path) if model.media_path is not None else None,
            amount=model.amount,
            description=model.description
        ) for model in models)

    def __dto_to_model(self, *dto: Product) -> tuple[ProductBase, ...]:
        return tuple(ProductBase(
            id=product.table_id if product.table_id is not None else None,
            product_id=product.product_id,
            autor_id=str(product.autor_id),
            name_product=product.name_product,
            catalog=product.catalog,
            price=float(product.price),
            media_path=[str(obj.path) for obj in product.media_path] if product.media_path is not None else None,
            amount=product.amount,
            description=product.description
        ) for product in dto)

    async def get_products_by_catalog(self, catalog: str) -> tuple[Product, ...]:
        products = await self._product_repo.get_products_by_catalog(catalog)
        return self.__model_to_dto(*products)

    async def get_products_by_user(self, user_id: int) -> tuple[Product, ...]:
        products = await self._product_repo.get_products_by_user_id(user_id)
        return self.__model_to_dto(*products)

    def _generate_product_id(self) -> int:
        return int(time.time() * 1000)

    def _processing_create_product(self, product: Product, user_id: int) -> Product:
        product.product_id = self._generate_product_id()
        product.autor_id = user_id
        product.amount = 1
        return product

    async def create_product(self, product: Product, user_id) -> bool:
        product = self._processing_create_product(product, user_id)
        product_model = self.__dto_to_model(product)[0]
        await self._product_repo.create_product(product_model)

        return True

    async def delete_product(self, product_id: int) -> None:
        await self._product_repo.delete_product(product_id)

    async def edit_product(self, product: Product) -> bool:
        model_product = self.__dto_to_model(product)[0]
        await self._product_repo.update_product(model_product)

        return True


class ProductPayManager:
    pass
