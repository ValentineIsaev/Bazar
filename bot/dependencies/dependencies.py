from pathlib import Path
from aiogram import Bot

from bot.managers.product_managers import ProductManager, InputProductManager, ProductCategoryManager

from bot.managers.catalog_manager import CatalogManager
from bot.storage.local_media_data import TelegramMediaLocalConsolidator


from bot.services.mediator_chat import MediatorService
from bot.managers.mediator_manager import MediatorManager
from bot.components.mediator_render import MediatorTelegramRenderer
from bot.types.utils import MessageSetting


def set_product_manager(data: dict):
    session = data['db_session']

    return ProductManager(session)

def set_input_product_manager(data: dict):
    fsm_storage = data['fsm_storage']

    return InputProductManager(fsm_storage)

def set_product_category_catalog_manager(data: dict):
    session = data['db_session']

    return ProductCategoryManager(session)

def set_catalog_manager(data: dict):
    fsm_storage = data['fsm_storage']

    return CatalogManager(fsm_storage)


mediator_service = MediatorService()
mediator_renderer = MediatorTelegramRenderer()
def set_mediator_manager(data: dict):
    session = data['db_session']

    return MediatorManager[MessageSetting](session, mediator_renderer, mediator_service)

class SetterMediaConsolidator:
    def __init__(self, bot: Bot, temp_storage_path: Path, perm_storage_path: Path):
        self._consolidator = TelegramMediaLocalConsolidator(bot, temp_storage_path,
                                                            perm_storage_path)

    def __call__(self, *args, **kwargs):
        return self._consolidator
