from aiogram.filters import and_f

from bot.handlers.buyer.templates.fsm_states import BuyerStates
from bot.handlers.buyer.templates.keyboard import *
from bot.managers.session_manager.session import UserSession
from bot.services.product.services import CatalogMenuService
from bot.utils.helper import get_data_state
from bot.handlers.handlers_import import *
from bot.handlers.utils import repack_choice_catalog_data
from bot.managers.catalog_manager.catalog_managers import ProductCatalogManager
from bot.handlers.utils import create_menu_catalog, send_catalog_message
from bot.services.product.services import ProductService

from bot.utils.message_utils.keyboard_utils import parse_callback, create_callback
from bot.configs.constants import UserTypes
from bot.constants.redis_keys import FSMKeys
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.utils.message_utils.message_setting_classes import MessageSetting
from bot.utils.message_utils.message_utils import send_message


buyer_router = Router()


@buyer_router.callback_query(and_f(CallbackFilter(scope='buy_product'),
                                   TypeUserFilter(UserTypes.BUYER)))
async def buy_product_handler(cb: CallbackQuery, state: FSMContext, product_service: ProductService,
                              session: UserSession):
    scope, subscope, action = parse_callback(cb.data)
    new_message: MessageSetting | None = None
    if subscope == 'choice_product':
        if action == 'start':
            await state.set_state(BuyerStates.BuyProduct.look_product)

            new_message = await create_menu_catalog(state, create_callback(scope=scope,
                                                                           subscope=subscope,
                                                                           action='choice_catalog'),
                                                    product_service)
        elif action.startswith('choice_catalog'):
            selected_catalog = await repack_choice_catalog_data(state, cb.data)
            products = product_service.get_products(selected_catalog)
            catalog_manager = ProductCatalogManager(products)
            new_message = catalog_manager.create_message()
            await state.update_data(**{FSMKeys.CATALOG_MANAGER: catalog_manager})
    elif subscope == 'buy_product':
        if action == 'choice_product':
            catalog: CatalogMenuService
            (catalog,) = await get_data_state(state, FSMKeys.CATALOG_MANAGER)
            product = catalog.get_catalogs()[0]

            await state.set_state(BuyerStates.BuyProduct.payment_product)
            new_message = MessageSetting(text='Оплатите товар.', keyboard=UNDO_BUY_PRODUCT)
        elif action == 'back':
            catalog_manager: ProductCatalogManager
            (catalog_manager,) = await get_data_state(state, FSMKeys.CATALOG_MANAGER)
            await send_catalog_message(session, cb.bot, catalog_manager.create_message())
    elif subscope == 'info_product':
        if action == 'send_answer':
            pass

    if new_message is not None:
        await send_message(session, cb.bot, new_message)
