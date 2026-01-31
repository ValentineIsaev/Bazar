from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from ..messages import *
from ..fsm import EDIT_PRODUCT_MESSAGES, EditProductStates
from .input_fields_product_handler import add_catalog_processing

from bot.constants.redis_keys import StorageKeys
from bot.constants.user_constants import TypesUser

from bot.types.storage import TelegramMediaLocalConsolidator, FSMStorage
from bot.types.middlewares import InputMediaMiddleWare
from bot.types.utils import CallbackSetting
from bot.utils.message_utils import send_message
from bot.utils.filters import CallbackFilter, TypeUserFilter

from bot.services.catalog_service import CatalogMenuService
from bot.services.product import Product
from bot.managers.catalog_manager import CatalogManager
from bot.managers.product_managers import InputProductManager, ProductCategoryManager, ProductManager

from bot.components.catalog_renderer import ChooseProductCatalogRenderer, SortCategoryCatalogRenderer
from bot.components.product_renderer import seller_product_renderer


router = Router()


async def _start_edit(action: str, input_product_manager: InputProductManager,
                      media_consolidator: TelegramMediaLocalConsolidator,
                      fsm_storage: FSMStorage, bot: Bot, state: FSMContext):
    is_send_new = False
    if action == 'start_edit_exist':
        is_send_new = True
        product = await input_product_manager.get_product()
        product_msg = seller_product_renderer.render_product(product, media_consolidator)
        await send_message(fsm_storage, bot, product_msg, False)
    await state.set_state(EditProductStates.choose_param)
    await send_message(fsm_storage, bot, EDIT_PRODUCT_MESSAGE, is_send_new)


@router.callback_query(CallbackFilter('product','edit'),
                              TypeUserFilter(TypesUser.SELLER))
async def edit_product_handler(cb: CallbackQuery, bot: Bot, state: FSMContext, fsm_storage: FSMStorage,
                               input_product_manager: InputProductManager, catalog_manager: CatalogManager,
                               products_catalog_manager: ProductCategoryManager,
                               media_consolidator: TelegramMediaLocalConsolidator,
                               media_middleware: InputMediaMiddleWare):
    _, _, action = CallbackSetting.decode_callback(cb.data)

    new_msg: MessageSetting | None = None
    new_state: State | None = None
    is_send_new: bool = False
    if action.startswith('start'):
        await _start_edit(action, input_product_manager, media_consolidator, fsm_storage, bot, state)

    elif action == 'catalog':
        new_state = EditProductStates.EditParam.edit_catalog
        await state.set_state(new_state)
        new_msg = await add_catalog_processing(CallbackSetting('product', 'add_catalog', 'start').callback, cb.message, state, fsm_storage, input_product_manager, catalog_manager,
                          products_catalog_manager, media_middleware, media_consolidator)

    elif action == 'name':
        new_state = EditProductStates.EditParam.edit_name

    elif action == 'price':
        new_state = EditProductStates.EditParam.edit_price

    elif action == 'media':
        new_state = EditProductStates.EditParam.edit_photo

    elif action == 'description':
        new_state = EditProductStates.EditParam.edit_description

    else:
        raise ValueError('The new state is not specified!')

    await state.set_state(new_state)
    if new_msg is None:
        new_msg = EDIT_PRODUCT_MESSAGES.get(new_state)

    if new_msg is not None:
        await send_message(fsm_storage, bot, new_msg, is_send_new)


async def _start_delete(input_product_manager: InputProductManager, fsm_storage, bot: Bot,
                        media_consolidator: TelegramMediaLocalConsolidator):
    product = await input_product_manager.get_product()
    await send_message(fsm_storage, bot, seller_product_renderer.render_product(product, media_consolidator), False)

    await send_message(fsm_storage, bot, DELETE_PRODUCT_MESSAGE)


@router.callback_query(CallbackFilter(scope='product', subscope='delete_product'), TypeUserFilter(TypesUser.SELLER))
async def delete_product(cb: CallbackQuery, bot: Bot, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                         product_manager: ProductManager, media_consolidator: TelegramMediaLocalConsolidator):
    _, _, action = CallbackSetting.decode_callback(cb.data)
    new_msg: MessageSetting | None = None
    is_send_new = False
    if action == 'start':
        await _start_delete(input_product_manager, fsm_storage, bot, media_consolidator)
    elif action == 'delete':
        product = await input_product_manager.get_product()
        await product_manager.delete_product(product.product_id)

        await send_message(fsm_storage, bot, SUCCESSFUL_DELETE_PRODUCT, False)
        is_send_new = True
        new_msg = POST_DELETE_PRODUCT_MSG

    if new_msg is not None:
        await send_message(fsm_storage, bot, new_msg, is_send_new)

def filter_by_catalog(data: tuple[int, Product], **kwargs):
    catalog_name = kwargs.get('catalog_name')
    return data[1].catalog == catalog_name

async def _start_product_handler(cb: str, user_id: int, state: FSMContext, product_manager: ProductManager,
                                 catalog_manager: CatalogManager) -> MessageSetting:
    async def start_choice_product(mode_state: State):
        if await state.get_state() != mode_state:
            user_products_ = await product_manager.get_products_by_user(user_id)
            products_ = tuple((p.table_id, p) for p in user_products_)

            catalog_service = CatalogMenuService(products_, 5)
            catalog_renderer = ChooseProductCatalogRenderer(CallbackSetting(scope, subscope, 'choice_product'))

            await catalog_manager.set_catalog_service(catalog_service)
            await catalog_manager.set_renderer(catalog_renderer)

            await state.set_state(mode_state)

    scope, subscope, action = CallbackSetting.decode_callback(cb)
    new_msg: MessageSetting | None = None

    if action == 'start_edit':
        # Choice product for edit
        await start_choice_product(EditProductStates.edit_product)
        new_msg = await catalog_manager.render_message()

    elif action == 'start_delete':
        # Choice product for delete
        await start_choice_product(EditProductStates.delete_product)
        new_msg = await catalog_manager.render_message()

    return new_msg

@router.callback_query(or_f(CallbackFilter(scope='product', subscope='choose_product', action='start_edit'),
                            CallbackFilter(scope='product', subscope='choose_product', action='start_delete')))
async def start_edit_user_products(cb: CallbackQuery, state: FSMContext, product_manager: ProductManager,
                                   catalog_manager: CatalogManager, fsm_storage: FSMStorage):
    new_msg = await _start_product_handler(cb.data, cb.from_user.id, state, product_manager, catalog_manager)
    if new_msg is not None: await send_message(fsm_storage, cb.bot, new_msg, False)

@router.callback_query(CallbackFilter(scope='product', subscope='choose_product'), TypeUserFilter(TypesUser.SELLER))
async def choose_product(cb: CallbackQuery, bot: Bot, state: FSMContext, fsm_storage: FSMStorage,
                         input_product_manager: InputProductManager, catalog_manager: CatalogManager,
                         media_consolidator: TelegramMediaLocalConsolidator):

    scope, subscope, action = CallbackSetting.decode_callback(cb.data)
    new_state: State | None
    new_msg: MessageSetting | None
    new_msg, new_state = None, None

    if action.startswith('choice_product'):
        # Edit or Delete certain product
        product: Product = await catalog_manager.get_catalog_by_callback(CallbackSetting(*CallbackSetting.decode_callback(cb.data)))
        await input_product_manager.set_product(product)

        now_state = await state.get_state()
        if now_state == EditProductStates.edit_product:
            await _start_edit('start_edit_exist', input_product_manager, media_consolidator, fsm_storage, bot,
                              state)

        elif now_state == EditProductStates.delete_product:
            await _start_delete(input_product_manager, fsm_storage, bot, media_consolidator)

    if new_state is not None:
        await state.set_state(new_state)

    if new_msg is not None:
        await send_message(fsm_storage, bot, new_msg, False)

@router.callback_query(CallbackFilter(scope='seller_product_catalog', subscope='filtering'))
async def filter_product_catalog(cb: CallbackQuery, bot: Bot, catalog_manager: CatalogManager,
                                 fsm_storage: FSMStorage, state: FSMContext, product_manager: ProductManager):
    async def filter_catalog(filter_name: str, **filter_data) -> MessageSetting:
        user_product_catalog = await fsm_storage.get_value(StorageKeys.EditProduct.USER_PRODUCT_CATALOG)
        await catalog_manager.set_catalog_service(user_product_catalog)

        await catalog_manager.filter_catalog(filter_name, **filter_data)
        await catalog_manager.set_renderer(ChooseProductCatalogRenderer(CallbackSetting(scope, subscope,
                                                                                        'choice_product')))

        new_cb = (CallbackSetting(scope, subscope, 'start_edit') if await state.get_state() == EditProductStates.edit_product \
            else CallbackSetting(scope, subscope, 'start_delete')).callback
        return await _start_product_handler(new_cb, cb.from_user.id, state, product_manager, catalog_manager)

    scope, subscope, action = CallbackSetting.decode_callback(cb.data)
    new_msg: MessageSetting|None = None
    if action == 'start':
        # Send filters
        new_msg = SET_SEARCH_DATA_MESSAGE
        if not await catalog_manager.is_set_filters():
            await catalog_manager.set_filters({'catalog': filter_by_catalog})

    elif action == 'set_catalog_filter':
        products = await catalog_manager.get_row_catalog()
        product_users_category = set(p.catalog for _, p in products)
        catalog_category_service = CatalogMenuService(tuple(zip(tuple(range(len(product_users_category))),
                                                                product_users_category)), 5)

        await fsm_storage.update_value(StorageKeys.EditProduct.USER_PRODUCT_CATALOG,
                                       await catalog_manager.get_catalog_service())
        await catalog_manager.set_catalog_service(catalog_category_service)
        await catalog_manager.set_renderer(SortCategoryCatalogRenderer(CallbackSetting(scope, subscope, 'filter_by_catalog')))

        new_msg = await catalog_manager.render_message()

    elif action.startswith('filter_by_catalog'):
        user_catalog = await catalog_manager.get_catalog_by_callback(
            CallbackSetting(*CallbackSetting.decode_callback(cb.data)))
        new_msg = await filter_catalog('catalog', catalog_name=user_catalog)

    if new_msg is not None:
        await send_message(fsm_storage, bot, new_msg, False)