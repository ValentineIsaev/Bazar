from .models import CatalogMenu, Product


class ProductService:
    MAX_VISIBLE_CATALOGS = 20

    @staticmethod
    def get_product_catalog() -> CatalogMenu:
        return CatalogMenu((
            "Электроника",
            "Одежда",
            "Обувь",
            "Дом и сад",
            "Красота и уход",
            "Спорт и фитнес",
            "Автотовары",
            "Книги",
            "Игрушки и игры",
            "Зоотовары",
            "Бытовая техника",
            "Строительство и ремонт",
            "Продукты питания",
            "Товары для офиса",
            "Аксессуары",
            "Туризм и отдых",
            "Детские товары",
            "Цифровые товары",
            "Антиквариат и коллекции",
            "Ювелирные изделия",
            "Табачные изделия",
            'Продуктовые изделия'
        ),
            ProductService.MAX_VISIBLE_CATALOGS
            )

    @staticmethod
    def get_products(catalog: str) -> CatalogMenu:
        return CatalogMenu((
            Product(name='Parliament', price='300', description='Дорогие приятные крепкие сигареты'),
                    Product(name='Philipmorris', price='200', description='Вкусные сигареты с кнопкой'),
                    Product(name='Camel', price='222', description='Старый добрый верблюд')
        ),
        page_capacity=1)

    @staticmethod
    def send_product(product: Product) -> None:
        pass

    @staticmethod
    def get_product(product_id: int) -> Product:
        pass
