from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from bot.types.storage import MediaConsolidator

from bot.services.product import Product

RenderType = TypeVar('RenderType')
class ProductRenderer(ABC, Generic[RenderType]):
    @abstractmethod
    def render_product(self, product: Product, media_consolidator: MediaConsolidator) -> RenderType:
        pass
