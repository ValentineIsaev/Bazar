from bot.managers.product_managers import ProductManager, InputProductManager, ProductCategoryCatalogManager

from bot.managers.catalog_manager import CatalogManager


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
