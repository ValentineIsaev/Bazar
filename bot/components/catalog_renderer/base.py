from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from bot.services.catalog_service import CatalogMenuService

RenderType = TypeVar('RenderType')
Callback = TypeVar('Callback')

class CatalogRenderer(ABC, Generic[RenderType, Callback]):
    @abstractmethod
    def get_id_by_callback(self, callback: Callback) -> int:
        pass

    @abstractmethod
    def render_message(self, catalog_service: CatalogMenuService) -> RenderType:
        pass