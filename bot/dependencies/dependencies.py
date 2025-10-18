from bot.managers.product_managers import ProductManager


def get_product_manager(data: dict):
    storage = data['storage']
    session = data['db_session']

    return ProductManager(storage, session)
