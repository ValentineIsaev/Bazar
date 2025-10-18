from bot.services.product import InputProductService, Product


class ProductManager:
    def __init__(self):
        self._product: InputProductService | None = None

    def get_catalog(self):
        pass

    def get_product(self):
        pass

    def get_products(self):
        pass

    def create_product(self):
        pass

    def new_product(self) -> None:
        """
        The method for creating a service for filling in data about a new product.
        """
        self._product = InputProductService()

    @property
    def product(self) -> InputProductService | None:
        """Getter a service for filling in data about a new product."""
        return self._product