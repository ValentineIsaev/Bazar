from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.product import InputProductService, Product
from bot.storage.redis import Storage

from bot.constants.redis_keys import UserSessionKeys


class ProductManager:
    def __init__(self, storage: Storage, session: AsyncSession):
        self._storage = storage
        self._session = session

        self._product: InputProductService | None = None

    def get_catalogs(self):
        pass

    def get_product(self):
        pass

    def get_products(self, catalog: str):
        pass

    def create_product(self):
        pass

    def new_product(self) -> None:
        """
        The method for creating a service for filling in data about a new product.
        """
        self._product = InputProductService()
        self._storage.update_data(**{UserSessionKeys.INPUT_PRODUCT_SERVICE: self._product})

    async def add_value_product(self, field_name: str, value) -> str | None:
        self._product = await self._storage.get_value(UserSessionKeys.INPUT_PRODUCT_SERVICE)
        if self._product is None:
            raise TypeError('Product service is None!')

        result = self._product.add_value(field_name, value)
        if result is not None:
            await self._storage.update_data(**{UserSessionKeys.INPUT_PRODUCT_SERVICE: self._product})

        return result

    async def get_input_product(self) -> Product | None:
        """Getter a service for filling in data about a new product."""
        self._product = await self._storage.get_value(UserSessionKeys.INPUT_PRODUCT_SERVICE)
        if self._product is None:
            raise TypeError('Product service is None!')
        return self._product.product
