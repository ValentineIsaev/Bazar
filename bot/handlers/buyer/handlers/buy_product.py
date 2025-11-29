from aiogram.filters import and_f

from bot.constants.redis_keys import UserSessionKeys
from bot.handlers.buyer.templates.fsm_states import BuyerStates
from bot.handlers.buyer.templates.keyboard import BUY_PRODUCT_KEYBOARD
from bot.services.catalog_service import CatalogMenuService
from bot.storage.local_media_data import TelegramMediaLocalConsolidator
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
from bot.components.catalog_renderer import ProductCatalogRenderer
from bot.types.utils import CallbackSetting, MessageSetting

from bot.handlers.utils import render_product_message


buyer_router = Router()


@buyer_router.callback_query(and_f(CallbackFilter(scope='buy_product'),
                                   TypeUserFilter(UserTypes.BUYER)))
async def buy_product_handler(cb: CallbackQuery, state: FSMContext, product_manager: ProductManager,
                              fsm_storage: FSMStorage,
                              catalog_manager: CatalogManager,
                              product_category_catalog_manager: ProductCategoryCatalogManager,
                              media_consolidator: TelegramMediaLocalConsolidator):
    scope, subscope, action = CallbackSetting.decode_callback(cb.data)
    new_message: MessageSetting | None = None
    if subscope == 'choice_product':
        if action == 'start':
            await state.set_state(BuyerStates.BuyProduct.look_product)
            await set_category_catalog_manager(catalog_manager,
                                                             product_category_catalog_manager,
                                                             CallbackSetting(scope, subscope, 'choice_catalog'))
            new_message = await catalog_manager.render_message()

        elif action.startswith('choice_catalog'):
            selected_catalog = await catalog_manager.get_catalog_by_callback(cb.data)
            products = product_manager.get_products_by_catalog(selected_catalog)

            catalog_service = CatalogMenuService(tuple((p.product_id, p) for p in products), 1)
            catalog_renderer = ProductCatalogRenderer(callback_prefix=CallbackSetting('buy_product',
                                                                                      'buy',
                                                                                      'start'),
                                                      media_consolidator=media_consolidator)

            await catalog_manager.set_catalog_service(catalog_service)
            await catalog_manager.set_renderer(catalog_renderer)

            new_message = await catalog_manager.render_message()
    elif subscope == 'buy':
        temp_product = await fsm_storage.get_value(UserSessionKeys.TEMP_PRODUCT)
        if action.startswith('start'):
            temp_product = await catalog_manager.get_catalog_by_callback(cb.data)
            new_message = render_product_message(temp_product, media_consolidator, BUY_PRODUCT_KEYBOARD)
        elif action == 'back':
            new_message = await catalog_manager.render_message()
            temp_product = None
        elif action == 'buy':
            product_manager.buy_product(temp_product.product_id, cb.from_user.id)
            temp_product = None
            new_message = MessageSetting(text='Куплено')

        await fsm_storage.update_value(UserSessionKeys.TEMP_PRODUCT, temp_product)

    elif subscope == 'info_product':
        if action == 'send_answer':
            pass

    if new_message is not None:
        await send_message(fsm_storage, cb.bot, new_message)
