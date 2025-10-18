from dataclasses import dataclass

from bot.utils.cache_utils.operators import CacheMediaOperator
from bot.utils.message_utils.message_setting_classes import MediaSetting


@dataclass()
class Product:
    id_seller: int = None

    name: str | None = None
    price: str | None = None
    catalog: str | None = None
    description: str | None = None
    media: CacheMediaOperator | None | MediaSetting = None
