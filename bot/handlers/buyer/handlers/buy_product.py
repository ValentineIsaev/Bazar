from aiogram.filters import and_f

from bot.handlers.handlers_import import *
from bot.handlers.utils import create_product_catalog, create_catalog
from bot.utils.message_utils.catalog_utils import repack_choice_catalog_data
from bot.services.product.services import ProductService

from bot.utils.message_utils.keyboard_utils import parse_callback, create_callback
from bot.configs.constants import ParamFSM, UserTypes
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.utils.message_utils.message_setting_classes import MessageSetting
from bot.utils.message_utils.message_utils import send_message

buyer_router = Router()


@buyer_router.callback_query(and_f(CallbackFilter(scope='buy_product'),
                                   TypeUserFilter(UserTypes.BUYER)))
async def buy_product_handler(cb: CallbackQuery, state: FSMContext):
    scope, subscope, action = parse_callback(cb.data)
    new_message: MessageSetting | None = None
    if subscope == 'choice_product':
        if action == 'start':
            new_message = await create_product_catalog(state, create_callback(scope=scope,
                                                                        subscope=subscope,
                                                                        action='choice_catalog'))
        elif action.startswith('choice_catalog'):
            selected_catalog = await repack_choice_catalog_data(cb.data, state)
            products = ProductService.get_products(selected_catalog)
            new_message = await create_catalog(state, create_callback(scope=scope,
                                                                      subscope=subscope,
                                                                      action='choice_product'), products)

    if new_message is not None:
        await send_message(state, cb.bot, new_message)
