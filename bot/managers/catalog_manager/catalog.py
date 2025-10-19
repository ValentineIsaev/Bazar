from bot.services.catalog_service import CatalogMenuService
from bot.components.catalog_renderer import CatalogRenderer

from bot.storage.redis import Storage

from bot.constants.redis_keys import FSMKeys
from bot.managers.base import StorageManager

from bot.utils.decorators import require_field
from bot.utils.message_utils.message_setting_classes import MessageSetting

from typing import Any


class CatalogManager(StorageManager):
    _SCROLL_NEXT = 'next'
    _SCROLL_BACK = 'back'

    def __init__(self, session_storage: Storage):
        super().__init__(session_storage)

        self._renderer: CatalogRenderer | None = None
        self._catalog_service: CatalogMenuService | None = None

    async def set_renderer(self, renderer: CatalogRenderer):
        await self._storage.update_value(FSMKeys.CatalogData.CATALOG_RENDERER, renderer)
        self._renderer = renderer

    async def set_catalog_service(self, catalog_service: CatalogMenuService):
        await self._storage.update_value(FSMKeys.CatalogData.CATALOG_SERVICE, catalog_service)
        self._catalog_service = catalog_service

    @require_field('_catalog_service', FSMKeys.CatalogData.CATALOG_SERVICE)
    async def scroll_catalog(self, mode: str):
        if mode == self._SCROLL_NEXT:
            self._catalog_service.next_page()
        elif mode == self._SCROLL_BACK:
            self._catalog_service.back_page()
        else:
            raise ValueError(f'Mode {mode} is wrong. Or {self._SCROLL_NEXT}, or {self._SCROLL_BACK}')

        await self._storage.update_value(FSMKeys.CatalogData.CATALOG_SERVICE, self._catalog_service)

    @require_field('_catalog_service', FSMKeys.CatalogData.CATALOG_SERVICE)
    async def get_page(self) -> tuple:
        return self._catalog_service.get_page_catalogs()

    @require_field('_catalog_service', FSMKeys.CatalogData.CATALOG_SERVICE)
    @require_field('_renderer', FSMKeys.CatalogData.CATALOG_RENDERER)
    async def render_message(self) -> MessageSetting:
        return self._renderer.render_message(self._catalog_service)

    @require_field('_catalog_service', FSMKeys.CatalogData.CATALOG_SERVICE)
    @require_field('_renderer', FSMKeys.CatalogData.CATALOG_RENDERER)
    async def get_catalog_by_callback(self, callback: str) -> Any:
        id_element = self._renderer.get_id_by_callback(callback)
        return self._catalog_service.get_element_by_id(id_element)


