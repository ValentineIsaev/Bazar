from typing import Any, Generic, Callable
from enum import Enum

from ..base import StorageManager, storage_field, set_storage_field

from bot.constants.redis_keys import StorageKeys

from bot.types.storage import Storage

from bot.services.catalog_service import CatalogMenuService
from bot.components.catalog_renderer import CatalogRenderer, Callback, RenderType


class ScrollModes(Enum):
    SCROLL_NEXT = 'next'
    SCROLL_BACK = 'back'


class CatalogManager(StorageManager, Generic[RenderType, Callback]):
    def __init__(self, session_storage: Storage):
        super().__init__(session_storage)

        self._renderer: CatalogRenderer | None = None
        self._catalog_service: CatalogMenuService | None = None

    @property
    def is_set_require_fields(self) -> bool:
        return self._renderer is not None and self._catalog_service is not None

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def is_set_filters(self) -> bool:
        return self._catalog_service.is_set_filters

    @set_storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def set_catalog_service(self, catalog_service: CatalogMenuService):
        self._catalog_service = catalog_service

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def get_catalog_service(self) -> CatalogMenuService:
        return self._catalog_service

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def set_filters(self, filters: dict[str, Callable[[Any, dict], bool]]):
        self._catalog_service.set_filters(filters)
        await self._storage.update_value(StorageKeys.CatalogData.CATALOG_SERVICE, self._catalog_service)

    @set_storage_field('_renderer', StorageKeys.CatalogData.CATALOG_RENDERER)
    async def set_renderer(self, renderer: CatalogRenderer):
        self._renderer = renderer

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def filter_catalog(self, filter_name: str, **filter_data):
        self._catalog_service.filter_catalog(filter_name, **filter_data)

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def reset_filter(self):
        self._catalog_service.reset_filter()

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def get_row_catalog(self) -> tuple[tuple[int, Any], ...]:
        return self._catalog_service.get_raw_catalog()

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def get_all(self) -> tuple[tuple[int, Any], ...]:
        return self._catalog_service.get_all()

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def scroll_catalog(self, mode: ScrollModes):
        if mode == ScrollModes.SCROLL_NEXT:
            self._catalog_service.next_page()
        elif mode == ScrollModes.SCROLL_BACK:
            self._catalog_service.back_page()
        else:
            raise ValueError(f'Mode {mode.value} is wrong. Or {ScrollModes.SCROLL_NEXT.value}, '
                             f'or {ScrollModes.SCROLL_NEXT.value}')

        await self._storage.update_value(StorageKeys.CatalogData.CATALOG_SERVICE, self._catalog_service)

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    async def get_page(self) -> tuple:
        return self._catalog_service.get_page_catalogs()

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    @storage_field('_renderer', StorageKeys.CatalogData.CATALOG_RENDERER)
    async def render_message(self) -> RenderType:
        return self._renderer.render_message(self._catalog_service)

    @storage_field('_catalog_service', StorageKeys.CatalogData.CATALOG_SERVICE)
    @storage_field('_renderer', StorageKeys.CatalogData.CATALOG_RENDERER)
    async def get_catalog_by_callback(self, callback: Callback) -> Any:
        # Callback much have full elements

        id_element = self._renderer.get_id_by_callback(callback)
        return self._catalog_service.get_element_by_id(id_element)


