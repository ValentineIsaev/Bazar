from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, StateFilter, or_f, and_f
from aiogram.fsm.context import FSMContext

from ..messages import *
from ..fsm import PRODUCT_STATES_DATA, StateData, AddProductStates, EditProductStates, TypeStates

from bot.constants.user_constants import TypesUser

from bot.types.middlewares import InputMediaMiddleWare
from bot.types.storage import FSMStorage, TelegramMediaLocalConsolidator, LocalObjPath
from bot.types.utils import CallbackSetting

from bot.utils.message_utils import send_message
from bot.utils.exception import UnknownCallback
from bot.utils.filters import CallbackFilter, TypeUserFilter

from bot.managers.product_managers import InputProductManager, ProductManager, ProductCategoryManager
from bot.managers.catalog_manager import CatalogManager

from bot.components.product_renderer import seller_product_renderer
from bot.components.catalog_renderer import AddProductCatalogRenderer
from bot.components.errors_renderer import product_error_renderer


router = Router()


async def input_product_field(value: Any, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                              state: FSMContext, media_middleware: InputMediaMiddleWare) -> MessageSetting:

    state_data: StateData = PRODUCT_STATES_DATA.get(await state.get_state())
    error = await input_product_manager.add_value(state_data.field_name, value)
    if error is None:
        new_message = state_data.new_msg
        if state_data.next_state_type == TypeStates.INPUT_MEDIA_TYPE:
            new_message = await media_middleware.start_input(fsm_storage, new_message, 3)
        await state.set_state(state_data.next_state)
    else:
        new_message = product_error_renderer.render_error(error, value=value)

    return new_message

async def _input_value(msg: Message, value: Any, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                       state: FSMContext, media_middleware: InputMediaMiddleWare,
                       media_consolidator: TelegramMediaLocalConsolidator):
    new_msg = await input_product_field(value, fsm_storage, input_product_manager, state, media_middleware)
    if new_msg is not None:
        await send_message(fsm_storage, msg.bot, new_msg)

    await user_checking(msg, state, fsm_storage, input_product_manager, media_consolidator)

async def user_checking(msg: Message, state: FSMContext, fsm_storage: FSMStorage,
                         input_product_manager: InputProductManager,
                         media_consolidator: TelegramMediaLocalConsolidator,):
    if await state.get_state() == AddProductStates.user_checking:
        new_message = seller_product_renderer.render_product(await input_product_manager.get_product(),
                                                             media_consolidator)
        await send_message(fsm_storage, msg.bot, new_message)
        await send_message(fsm_storage, msg.bot, COMPLETE_ADD_PRODUCT_MESSAGE)


@router.callback_query(CallbackFilter(scope='product', subscope='save'), TypeUserFilter(TypesUser.SELLER))
async def save_product(cb: CallbackQuery, product_manager: ProductManager, input_product_manager: InputProductManager,
                       media_consolidator: TelegramMediaLocalConsolidator, fsm_storage: FSMStorage, bot: Bot):
    _, _, action = CallbackSetting.decode_callback(cb.data)

    product = await input_product_manager.get_product()

    if product.media_path is not None:
        objs = media_consolidator.get_obj_data(*product.media_path)
        product.media_path = await media_consolidator.save_perm_obj(objs)

    if product.table_id is not None:
        is_save = await product_manager.edit_product(product)
        complete_message = SUCCESSFUL_EDIT_PRODUCT_MESSAGE
        new_msg = POST_EDIT_PRODUCT_MESSAGE
    else:
        is_save = await product_manager.create_product(product, cb.from_user.id)
        complete_message = SUCCESSFUL_CREATE_PRODUCT_MESSAGE
        new_msg = POST_CREATE_PRODUCT_MESSAGE
    if is_save:
        await send_message(fsm_storage, bot, complete_message, False)
    await send_message(fsm_storage, bot, new_msg)


async def add_catalog_processing(cb: str, msg: Message, state: FSMContext, fsm_storage: FSMStorage,
                      input_product_manager: InputProductManager, catalog_manager: CatalogManager,
                      products_catalog_manager: ProductCategoryManager,
                      media_middleware: InputMediaMiddleWare,
                      media_consolidator: TelegramMediaLocalConsolidator) -> MessageSetting:
    scope, subscope, action = CallbackSetting.decode_callback(cb)
    new_message: MessageSetting | None = None

    if action == 'start':
        now_state: str = await state.get_state()
        if now_state != EditProductStates.EditParam.edit_catalog.state:
            await input_product_manager.new()
            await state.set_state(AddProductStates.choose_catalog)

        await catalog_manager.set_renderer(AddProductCatalogRenderer(CallbackSetting(scope,
                                                                                     subscope,
                                                                                     'choice_catalog')))
        await catalog_manager.set_catalog_service(await products_catalog_manager.get_category_products())

        new_message = await catalog_manager.render_message()

    elif action.startswith('choice_catalog'):
        selected_catalog = await catalog_manager.get_catalog_by_callback(CallbackSetting(*CallbackSetting.decode_callback(cb)))
        await send_message(fsm_storage, msg.bot, MessageSetting(text=SELECTED_CATALOG_TEXT.insert((selected_catalog,)),
                                     parse_mode=ParseModes.MARKDOWN_V2), False)
        await _input_value(msg, selected_catalog, fsm_storage, input_product_manager, state, media_middleware,
                           media_consolidator)
    else:
        raise UnknownCallback(cb)

    return new_message


@router.callback_query(CallbackFilter(scope='product', subscope='add_catalog'), TypeUserFilter(TypesUser.SELLER))
async def add_catalog_handler(cb: CallbackQuery, bot: Bot, state: FSMContext, fsm_storage: FSMStorage,
                              input_product_manager: InputProductManager, catalog_manager: CatalogManager,
                              products_catalog_manager: ProductCategoryManager,
                              media_middleware: InputMediaMiddleWare,
                              media_consolidator: TelegramMediaLocalConsolidator):
    new_msg = await add_catalog_processing(cb.data, cb.message, state, fsm_storage, input_product_manager, catalog_manager,
                      products_catalog_manager, media_middleware, media_consolidator)
    if new_msg is not None: await send_message(fsm_storage, bot, new_msg, False)


@router.message(StateFilter(AddProductStates.add_name,
                            AddProductStates.add_price,
                            AddProductStates.add_description,
                            EditProductStates.EditParam.edit_name,
                            EditProductStates.EditParam.edit_price,
                            EditProductStates.EditParam.edit_description))
async def input_text_fields(msg: Message, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                            state: FSMContext, media_middleware: InputMediaMiddleWare,
                            media_consolidator: TelegramMediaLocalConsolidator):
    await _input_value(msg, msg.text, fsm_storage, input_product_manager, state, media_middleware, media_consolidator)


@router.message(StateFilter(AddProductStates.add_photo,
                            EditProductStates.EditParam.edit_photo))
async def input_media_field(msg: Message, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                            state: FSMContext, media_middleware: InputMediaMiddleWare,
                            media: tuple[LocalObjPath, ...],
                            media_consolidator: TelegramMediaLocalConsolidator):
    await _input_value(msg, media, fsm_storage, input_product_manager, state, media_middleware, media_consolidator)
