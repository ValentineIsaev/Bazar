from dataclasses import dataclass

from bot.storage.local_media_data.dto import LocalObjPath


@dataclass()
class Product:
    table_id: int = None
    product_id: int = None
    autor_id: int = None

    name_product: str = None
    catalog: str = None
    price: float = None
    media_path: tuple[LocalObjPath, ...] = None
    amount: int = None
    description: str = None
