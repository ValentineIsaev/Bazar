from aiogram.filters import and_f

from bot.handlers.buyer.templates.fsm_states import BuyerStates
from bot.storage.redis import FSMStorage
from aiogram import Router
# from bot.components.catalog_renderer import ProductCatalogManager
from bot.handlers.utils import set_category_catalog_manager
from bot.managers.product_managers import ProductManager, ProductCategoryCatalogManager
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.configs.constants import UserTypes
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.utils.message_utils.message_utils import send_message

from bot.managers.catalog_manager import CatalogManager
from bot.types.utils import CallbackSetting, MessageSetting


buyer_router = Router()


@buyer_router.callback_query(and_f(CallbackFilter(scope='buy_product'),
                                   TypeUserFilter(UserTypes.BUYER)))
async def buy_product_handler(cb: CallbackQuery, state: FSMContext, product_manager: ProductManager,
                              fsm_storage: FSMStorage,
                              catalog_manager: CatalogManager,
                              product_category_catalog_manager: ProductCategoryCatalogManager):
    scope, subscope, action = CallbackSetting.decode_callback(cb.data)
    new_message: MessageSetting | None = None
    if subscope == 'choice_product':
        if action == 'start':
            await state.set_state(BuyerStates.BuyProduct.look_product)
            await set_category_catalog_manager(catalog_manager,
                                                             product_category_catalog_manager,
                                                             CallbackSetting(scope, subscope, 'choice_catalog'))
            new_message = await catalog_manager.render_message()

        # elif action.startswith('choice_catalog'):
        #     selected_catalog = catalog_manager.get_catalog_by_callback(cb.data)
        #     products = product_manager.get_products(selected_catalog)
        #     catalog_manager = ProductCatalogManager(products)
        #     new_message = catalog_manager
        #     new_message = catalog_manager.create_message()
        #     await fsm_storage.update_value(FSMKeys.CATALOG_MANAGER, catalog_manager)
    elif subscope == 'buy_product':
        if action == 'choice_product':
            pass
        elif action == 'back':
            new_message = await catalog_manager.render_message()
    elif subscope == 'info_product':
        if action == 'send_answer':
            pass

    if new_message is not None:
        await send_message(fsm_storage, cb.bot, new_message)
