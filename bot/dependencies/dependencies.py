from bot.managers.product_managers import ProductManager, InputProductManager, ProductCategoryCatalogManager

from bot.managers.catalog_manager import CatalogManager
from bot.storage.local_media_data import TelegramMediaLocalConsolidator
from bot.configs.configs import media_storage_data

from pathlib import Path
from aiogram import Bot

from bot.services.mediator_chat import MediatorService
from bot.managers.mediator_manager import MediatorManager
from bot.components.mediator_render import MediatorTelegramRenderer


def set_product_manager(data: dict):
    session = data['db_session']

    return ProductManager(session)

def set_input_product_manager(data: dict):
    fsm_storage = data['fsm_storage']
    session = data['db_session']

    return InputProductManager(fsm_storage, session)

def set_product_category_catalog_manager(data: dict):
    session = data['db_session']

    return ProductCategoryCatalogManager(session)

def set_catalog_manager(data: dict):
    fsm_storage = data['fsm_storage']

    return CatalogManager(fsm_storage)


mediator_service = MediatorService()
mediator_renderer = MediatorTelegramRenderer()
def set_mediator_manager(data: dict):
    session = data['db_session']

    return MediatorManager(session, mediator_renderer, mediator_service)


class SetterMediaConsolidator:
    def __init__(self, bot: Bot, temp_storage_path: Path, perm_storage_path: Path):
        self._consolidator = TelegramMediaLocalConsolidator(bot, temp_storage_path,
                                                            perm_storage_path)

    def __call__(self, *args, **kwargs):
        return self._consolidator

# def set_media_consolidator(data: dict):
#     bot = data['bot']
#     return TelegramMediaLocalConsolidator(bot, media_storage_data.TEMP_STORAGE_PATH,
#                                           media_storage_data.PERM_STORAGE_PATH)
