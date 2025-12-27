from aiogram.filters import StateFilter

from bot.constants.redis_keys import FSMKeys, UserSessionKeys
from bot.handlers.seller.templates.messages import EDIT_PRODUCT_MESSAGE, SUCCESSFUL_DELETE_PRODUCT, \
    DELETE_PRODUCT_MESSAGE
from bot.handlers.seller.templates.fsm import EditProductStates
from aiogram import Router, Bot

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from bot.managers.catalog_manager import CatalogManager
from bot.managers.product_managers import InputProductManager, ProductCategoryManager, ProductManager
from bot.storage.local_media_data import TelegramMediaLocalConsolidator
from bot.utils.message_utils.message_utils import MessageSetting, send_message
from bot.handlers.seller.templates.configs import FieldConfig
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.configs.constants import UserTypes
from bot.types.utils import CallbackSetting

from bot.components.catalog_renderer import ChooseProductCatalogRenderer, CategoryCatalogRenderer

from bot.storage.redis import FSMStorage

from bot.services.catalog_service import CatalogMenuService
from bot.services.product import Product

from .input_fields_product_handler import (add_catalog, add_media, add_price, add_name,
                                           add_description)
from bot.handlers.utils import render_product_message, delete_product_message
from ..templates.keyboards import ADD_PRODUCT_COMPLETE_KEYBOARD
from ..templates.messages import SET_SEARCH_DATA_MESSAGE, SET_NAME_SEARCH_PRODUCT_MSG
from ..templates.fsm import AddProductStates, EDIT_PRODUCT_MESSAGES

router = Router()


def new_callback_query(old_cb: CallbackQuery, new_callback_data: CallbackSetting):
    callback_cls_data = old_cb.__dict__.copy()
    callback_cls_data['data'] = new_callback_data.callback
    return old_cb.__class__(**callback_cls_data)


@router.callback_query(CallbackFilter('product','edit'),
                              TypeUserFilter(UserTypes.SELLER))
async def edit_product_handler(cb: CallbackQuery, bot: Bot, state: FSMContext, fsm_storage: FSMStorage,
                               input_product_manager: InputProductManager, catalog_manager: CatalogManager,
                               products_catalog_manager: ProductCategoryManager,
                               media_consolidator: TelegramMediaLocalConsolidator):
    _, _, action = CallbackSetting.decode_callback(cb.data)

    new_msg: MessageSetting | None = None
    new_state: State
    if action == 'start':
        new_state = EditProductStates.choose_param
        new_msg = EDIT_PRODUCT_MESSAGE

        product = await input_product_manager.get_product()
        product_msg = render_product_message(product, media_consolidator=media_consolidator)
        await send_message(fsm_storage, bot, product_msg)

        product_msg_id = await fsm_storage.get_value(UserSessionKeys.BOTS_MESSAGE_ID)
        product_media_msg_id = None if product.media_path is None else \
            await fsm_storage.get_value(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID)

        await fsm_storage.update_data(**{UserSessionKeys.PRODUCT_MESSAGE_ID: product_msg_id,
                                         UserSessionKeys.PRODUCT_MEDIA_MESSAGE_ID: product_media_msg_id})

    elif action == 'catalog':
        new_state = EditProductStates.EditParam.edit_catalog
        await state.set_state(new_state)

        new_cb = new_callback_query(cb, CallbackSetting('product', 'add_catalog', 'start'))
        await add_catalog(new_cb, bot, state, fsm_storage, input_product_manager, catalog_manager,
                          products_catalog_manager, media_consolidator)

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
        await send_message(fsm_storage, bot, new_msg)

@router.callback_query(CallbackFilter(scope='product', subscope='delete_product'), TypeUserFilter(UserTypes.SELLER))
async def delete_product(cb: CallbackQuery, bot: Bot, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                         product_manager: ProductManager):
    _, _, action = CallbackSetting.decode_callback(cb.data)
    if action == 'start':
        await send_message(fsm_storage, bot, DELETE_PRODUCT_MESSAGE)
    elif action == 'delete':
        product = await input_product_manager.get_product()
        await product_manager.delete_product(product.product_id)

        await send_message(fsm_storage, bot, SUCCESSFUL_DELETE_PRODUCT)
        await delete_product_message(fsm_storage, bot)


@router.callback_query(CallbackFilter(scope='product', subscope='choose_product'), TypeUserFilter(UserTypes.SELLER))
async def choose_product(cb: CallbackQuery, bot: Bot, state: FSMContext, fsm_storage: FSMStorage,
                         input_product_manager: InputProductManager, product_manager: ProductManager,
                         catalog_manager: CatalogManager, products_catalog_manager: ProductCategoryManager,
                         media_consolidator: TelegramMediaLocalConsolidator):

    async def start_choice_product():
        if not catalog_manager.is_set_require_fields:
            user_products_ = await product_manager.get_products_by_user(cb.from_user.id)
            catalog_service = CatalogMenuService(tuple((p.table_id, p) for p in user_products_), 5)
            catalog_renderer = ChooseProductCatalogRenderer(CallbackSetting(scope, subscope, 'choice_product'))

            await catalog_manager.set_catalog_service(catalog_service)
            await catalog_manager.set_renderer(catalog_renderer)
            await fsm_storage.update_value(FSMKeys.EditProduct.USER_PRODUCT_LIST, user_products_)

    scope, subscope, action = CallbackSetting.decode_callback(cb.data)
    new_state: State | None = None

    if action == 'start_edit':
        # Choice product for edit
        new_state = EditProductStates.edit_product
        await start_choice_product()
        print('edit_start')
        await send_message(fsm_storage, bot, await catalog_manager.render_message())

    elif action == 'start_delete':
        # Choice product for delete
        new_state = EditProductStates.delete_product
        await start_choice_product()
        await send_message(fsm_storage, bot, await catalog_manager.render_message())

    elif action.startswith('choice_product'):
        # Edit or Delete certain product
        product: Product = await catalog_manager.get_catalog_by_callback(cb.data)

        now_state = await state.get_state()
        await input_product_manager.set_product(product)
        if now_state == EditProductStates.edit_product.state:

            new_cb = new_callback_query(cb, CallbackSetting('product', 'edit', 'start'))
            await edit_product_handler(new_cb, bot, state, fsm_storage, input_product_manager, catalog_manager,
                                       products_catalog_manager, media_consolidator)

        elif now_state == EditProductStates.delete_product:
            new_cb = new_callback_query(cb, CallbackSetting('product', 'delete_product', 'start'))
            await delete_product(new_cb, bot, fsm_storage, input_product_manager, product_manager)

    elif action == 'set_choice':
        # Set sort products
        await send_message(fsm_storage, bot, SET_SEARCH_DATA_MESSAGE)

    elif action == 'start_set_catalog':
        # Choice catalog for sort products

        products: tuple[tuple[int, Product], ...] = await catalog_manager.get_all()
        product_users_category = set(p.catalog for (_, p) in products)

        u_products = await catalog_manager.get_all()
        await fsm_storage.update_value(FSMKeys.EditProduct.USER_PRODUCT_LIST, u_products)

        catalog_category_service = CatalogMenuService(tuple(zip(tuple(range(len(product_users_category))),
                                                                product_users_category)), 5)

        await catalog_manager.set_catalog_service(catalog_category_service)
        await catalog_manager.set_renderer(CategoryCatalogRenderer(CallbackSetting(scope, subscope, 'set_catalog')))

        await send_message(fsm_storage, bot, await catalog_manager.render_message())

    elif action.startswith('set_catalog'):
        # Sort products by catalog

        user_catalog = await catalog_manager.get_catalog_by_callback(cb.data)

        user_products: tuple[tuple[int, Product], ...] = await fsm_storage.get_value(FSMKeys.EditProduct.USER_PRODUCT_LIST)
        new_user_products = tuple(p for p in user_products if p[1].catalog == user_catalog)

        await fsm_storage.update_value(FSMKeys.EditProduct.USER_PRODUCT_LIST, new_user_products)

        await catalog_manager.set_catalog_service(CatalogMenuService(new_user_products, 1))
        await catalog_manager.set_renderer(ChooseProductCatalogRenderer(CallbackSetting(scope, subscope,
                                                                                        'choice_product')))

        new_cb = new_callback_query(cb, CallbackSetting(scope, subscope, 'start_edit')) \
            if await state.get_state() == EditProductStates.edit_product.state else (
            new_callback_query(cb, CallbackSetting(scope, subscope, 'start_delete')))
        await choose_product(new_cb, bot, state, fsm_storage, input_product_manager, product_manager, catalog_manager,
                             products_catalog_manager, media_consolidator)

    if new_state is not None:
        await state.set_state(new_state)
