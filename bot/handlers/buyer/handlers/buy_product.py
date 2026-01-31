from aiogram import Router
from aiogram.filters import and_f
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..fsm import BuyerStates

from bot.constants.redis_keys import StorageKeys
from bot.constants.user_constants import TypesUser

from bot.types.utils import CallbackSetting, MessageSetting
from bot.types.storage import TelegramMediaLocalConsolidator, FSMStorage

from bot.utils.message_utils import send_message, delete_media_message, send_text_message
from bot.utils.filters import CallbackFilter, TypeUserFilter

from bot.services.catalog_service import CatalogMenuService
from bot.managers.product_managers import ProductManager, ProductCategoryManager
from bot.managers.catalog_manager import CatalogManager

from bot.components.catalog_renderer import ProductCatalogRenderer, BuyerCategoryCatalogRenderer
from bot.components.product_renderer import buyer_product_renderer


buyer_router = Router()

@buyer_router.callback_query(and_f(CallbackFilter(scope='buy_product', subscope='choice_product'),
                                   TypeUserFilter(TypesUser.BUYER)))
async def choice_product(cb: CallbackQuery, state: FSMContext, catalog_manager: CatalogManager,
                         products_catalog_manager: ProductCategoryManager, product_manager: ProductManager,
                         media_consolidator: TelegramMediaLocalConsolidator, fsm_storage: FSMStorage):
    scope, subscope, action = CallbackSetting.decode_callback(cb.data)

    new_msg: None | MessageSetting = None
    if action == 'start':
        await state.set_state(BuyerStates.BuyProduct.look_product)

        await catalog_manager.set_catalog_service(await products_catalog_manager.get_category_products())
        await catalog_manager.set_renderer(BuyerCategoryCatalogRenderer(CallbackSetting(scope,
                                                                                        subscope,
                                                                                        'choice_catalog')))

        new_msg = await catalog_manager.render_message()

    elif action.startswith('choice_catalog'):
        await state.set_state(BuyerStates.scroll_products)
        selected_catalog = await catalog_manager.get_catalog_by_callback(CallbackSetting.from_str(cb.data))
        products = await product_manager.get_products_by_catalog(selected_catalog)

        catalog_service = CatalogMenuService(tuple((p.product_id, p) for p in products), 1)
        catalog_renderer = ProductCatalogRenderer(callback_prefix=CallbackSetting('buy_product',
                                                                                  'buy',
                                                                                  'start'),
                                                  media_consolidator=media_consolidator)

        await catalog_manager.set_catalog_service(catalog_service)
        await catalog_manager.set_renderer(catalog_renderer)

        new_msg = await catalog_manager.render_message()

    if new_msg is not None:
        await send_message(fsm_storage, cb.bot, new_msg, False)

@buyer_router.callback_query(and_f(CallbackFilter(scope='buy_product', subscope='buy'),
                                   TypeUserFilter(TypesUser.BUYER)))
async def buy_product_handler(cb: CallbackQuery, product_manager: ProductManager,
                              fsm_storage: FSMStorage,
                              catalog_manager: CatalogManager,
                              media_consolidator: TelegramMediaLocalConsolidator,
                              state: FSMContext):
    _, _, action = CallbackSetting.decode_callback(cb.data)
    new_message: MessageSetting | None = None
    temp_product = await fsm_storage.get_value(StorageKeys.TEMP_PRODUCT)
    if action.startswith('start'):
        temp_product = await catalog_manager.get_catalog_by_callback(CallbackSetting(*CallbackSetting.decode_callback(cb.data)))
        await send_text_message(fsm_storage, cb.bot,
                                buyer_product_renderer.render_product(temp_product, media_consolidator),
                                False)
    elif action == 'back_product':
        await state.set_state(BuyerStates.scroll_products)
        await send_message(fsm_storage, cb.bot, buyer_product_renderer.render_product(temp_product, media_consolidator), False)
    elif action == 'back':
        await send_text_message(fsm_storage, cb.bot, await catalog_manager.render_message(), False)
        temp_product = None
    elif action == 'buy':
        product_manager.buy_product(temp_product.product_id, cb.from_user.id)
        temp_product = None
        new_message = MessageSetting(text='Куплено')

    await fsm_storage.update_value(StorageKeys.TEMP_PRODUCT, temp_product)

    if new_message is not None:
        await send_message(fsm_storage, cb.bot, new_message)
