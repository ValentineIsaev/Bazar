from aiogram.filters import and_f

from bot.handlers.buyer.templates.fsm_states import BuyerStates
from bot.handlers.buyer.templates.keyboard import *
from bot.services.product.services import CatalogMenuService
from bot.utils.helper import get_data_state
from bot.handlers.handlers_import import *
from bot.utils.catalog_utils.catalog_utils import repack_choice_catalog_data, create_product_catalog, \
    create_catalog_message, send_catalog_message
from bot.handlers.utils import create_menu_catalog
from bot.services.product.services import ProductService

from bot.utils.message_utils.keyboard_utils import parse_callback, create_callback
from bot.configs.constants import UserTypes, ParamFSM
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.utils.message_utils.message_setting_classes import MessageSetting
from bot.utils.message_utils.message_utils import send_message


buyer_router = Router()


@buyer_router.callback_query(and_f(CallbackFilter(scope='buy_product'),
                                   TypeUserFilter(UserTypes.BUYER)))
async def buy_product_handler(cb: CallbackQuery, state: FSMContext, product_services: ProductService):
    scope, subscope, action = parse_callback(cb.data)
    new_message: MessageSetting | None = None
    if subscope == 'choice_product':
        if action == 'start':
            await state.set_state(BuyerStates.BuyProduct.look_product)

            new_message = await create_menu_catalog(state, create_callback(scope=scope,
                                                                           subscope=subscope,
                                                                           action='choice_catalog'))
        elif action.startswith('choice_catalog'):
            selected_catalog = await repack_choice_catalog_data(cb.data, state)
            products = product_services.get_products(selected_catalog)

            await create_product_catalog(state, cb.bot, products)
    elif subscope == 'buy_product':
        if action == 'choice_product':
            catalog: CatalogMenuService
            (catalog,) = await get_data_state(state, ParamFSM.BotMessagesData.CatalogData.CATALOG_MENU)
            product = catalog.get_catalogs()[0]

            await state.set_state(BuyerStates.BuyProduct.payment_product)
            new_message = MessageSetting(text='Оплатите товар.', keyboard=UNDO_BUY_PRODUCT)
        elif action == 'back':
            new_msg = await create_catalog_message(state)
            await send_catalog_message(state, cb.bot, new_msg)

    if new_message is not None:
        await send_message(state, cb.bot, new_message)
