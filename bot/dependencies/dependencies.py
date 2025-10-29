from bot.managers.product_managers import ProductManager, InputProductManager, ProductCategoryCatalogManager

from bot.managers.catalog_manager import CatalogManager
from bot.storage.local_media_data import TelegramMediaLocalConsolidator
from bot.configs.configs import media_storage_data


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

def set_media_consolidator(data: dict):
    bot = data['bot']
    return TelegramMediaLocalConsolidator(bot, media_storage_data.TEMP_STORAGE_PATH,
                                          media_storage_data.PERM_STORAGE_PATH)
