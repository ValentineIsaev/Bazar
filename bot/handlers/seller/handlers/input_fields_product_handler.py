from typing import Any, Callable

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram import F, Bot
from aiogram.filters import StateFilter, or_f

from bot.handlers.utils import (set_category_catalog_manager, get_media_objs,
                                render_product_message, render_invalidate_input_product_msg)
from bot.constants.callback import PASS_CALLBACK
from bot.configs.constants import UserTypes
from bot.utils.message_utils import *
from bot.utils.exception import UnknownCallback
from bot.utils.message_utils.keyboard_utils import *
from bot.utils.filters import CallbackFilter, TypeUserFilter

from bot.storage.redis import FSMStorage
from bot.managers.product_managers import InputProductManager, ProductManager, ProductCategoryManager
from bot.managers.catalog_manager import CatalogManager
from bot.types.utils import CallbackSetting

from bot.types.storage import TelegramMediaLocalConsolidator
from ..templates.configs import *
from ..templates.fsm import PRODUCT_STATES_DATA, StateData, AddProductStates, EditProductStates

from bot.services.product import ProductInputField, Product


router = Router()


async def input_product_field(msg: Message, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                                      state: FSMContext, value: Any, media_consolidator: TelegramMediaLocalConsolidator,
                              is_delete_user_message: bool=True):
    if is_delete_user_message:
        await msg.delete()

    state_data: StateData = PRODUCT_STATES_DATA.get(await state.get_state())

    result = await input_product_manager.add_value(state_data.field_name, value)
    if result is None:
        if state_data.next_state == AddProductStates.user_checking:
            new_message = render_product_message(await input_product_manager.get_product(),
                                                 media_consolidator, ADD_PRODUCT_COMPLETE_KEYBOARD)
            new_message.text = new_message.text + COMPLETE_ADD_PRODUCT_MESSAGE
        else:
            new_message = state_data.new_msg
        await state.set_state(state_data.next_state)
    else:
        new_message = render_invalidate_input_product_msg(result, value)

    if new_message is not None:
        await send_message(fsm_storage, msg.bot, new_message, False)


@router.callback_query(CallbackFilter(scope='product', subscope='save'), TypeUserFilter(UserTypes.SELLER))
async def save_product(cb: CallbackQuery, product_manager: ProductManager, input_product_manager: InputProductManager,
                       media_consolidator: TelegramMediaLocalConsolidator, fsm_storage: FSMStorage, bot: Bot):
    _, _, action = CallbackSetting.decode_callback(cb.data)

    product = await input_product_manager.get_product()

    if product.media_path is not None:
        objs = media_consolidator.get_obj_data(*product.media_path)
        product.media_path = await media_consolidator.save_perm_obj(objs)

    if product.table_id is not None:
        await product_manager.edit_product(product)
    else:
        await product_manager.create_product(product, cb.from_user.id)
    await send_message(fsm_storage, bot, SUCCESSFUL_SAVE_PRODUCT)


async def add_catalog(cb: CallbackQuery, bot: Bot, state: FSMContext, fsm_storage: FSMStorage,
                      input_product_manager: InputProductManager, catalog_manager: CatalogManager,
                      products_catalog_manager: ProductCategoryManager,
                      media_consolidator: TelegramMediaLocalConsolidator):
    scope, subscope, action = CallbackSetting.decode_callback(cb.data)
    new_message: MessageSetting | None
    is_send_new: bool
    new_message, is_send_new = None, True

    if action == 'start':
        now_state: str = await state.get_state()
        if now_state != EditProductStates.EditParam.edit_catalog.state:
            await input_product_manager.new()
            await state.set_state(AddProductStates.choose_catalog)

        await set_category_catalog_manager(catalog_manager, products_catalog_manager,
                                           CallbackSetting(scope,
                                                           subscope,
                                                           'choice_catalog'))
        new_message = await catalog_manager.render_message()

    elif action.startswith('choice_catalog'):
        selected_catalog = await catalog_manager.get_catalog_by_callback(cb.data)
        await input_product_field(cb.message, fsm_storage, input_product_manager, state, selected_catalog,
                                  media_consolidator,
                                  is_delete_user_message=False)
    else:
        raise UnknownCallback(cb.data)

    if new_message is not None:
        await send_message(fsm_storage, bot, new_message, is_send_new)


@router.callback_query(CallbackFilter(scope='product', subscope='add_catalog'), TypeUserFilter(UserTypes.SELLER))
async def add_catalog_handler(cb: CallbackQuery, bot: Bot, state: FSMContext, fsm_storage: FSMStorage,
                              input_product_manager: InputProductManager, catalog_manager: CatalogManager,
                              products_catalog_manager: ProductCategoryManager,
                              media_consolidator: TelegramMediaLocalConsolidator):
    await add_catalog(cb, bot, state, fsm_storage, input_product_manager, catalog_manager,
                      products_catalog_manager, media_consolidator)


async def add_name(msg: Message, state: FSMContext, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                   media_consolidator: TelegramMediaLocalConsolidator):
    await input_product_field(msg, fsm_storage, input_product_manager, state, msg.text, media_consolidator)


@router.message(StateFilter(AddProductStates.add_name, EditProductStates.EditParam.edit_name))
async def add_name_handler(msg: Message, state: FSMContext, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                   media_consolidator: TelegramMediaLocalConsolidator):
    await add_name(msg, state, fsm_storage, input_product_manager, media_consolidator)


async def add_description(msg: Message, state: FSMContext, fsm_storage: FSMStorage,
                          input_product_manager: InputProductManager,
                          media_consolidator: TelegramMediaLocalConsolidator):
    await input_product_field(msg, fsm_storage, input_product_manager, state, msg.text, media_consolidator)



@router.message(StateFilter(AddProductStates.add_description,
                                   EditProductStates.EditParam.edit_description))
async def add_description_handler(msg: Message, state: FSMContext, fsm_storage: FSMStorage,
                          input_product_manager: InputProductManager,
                          media_consolidator: TelegramMediaLocalConsolidator):
    await add_description(msg, state, fsm_storage, input_product_manager, media_consolidator)


async def add_media(msg: Message, state: FSMContext, fsm_storage: FSMStorage,
                          input_product_manager: InputProductManager,
                          media_consolidator: TelegramMediaLocalConsolidator):
    media = await get_media_objs(msg, fsm_storage, media_consolidator, PHOTO_INPUT_STOP_TEXT,
                                 PROCESS_INPUT_PHOTO_PRODUCT_MESSAGE, '/skip', 3)

    if media:
        await  input_product_field(msg, fsm_storage, input_product_manager, state, media, media_consolidator)


@router.message(or_f(F.photo, F.video, Command('skip'),
                     StateFilter(AddProductStates.add_photo,
                                        EditProductStates.EditParam.edit_photo)))
async def add_media_handler(msg: Message, state: FSMContext, fsm_storage: FSMStorage,
                    input_product_manager: InputProductManager,
                    media_consolidator: TelegramMediaLocalConsolidator):
    await add_media(msg, state, fsm_storage, input_product_manager, media_consolidator)


async def add_price(msg: Message, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                    state: FSMContext, media_consolidator: TelegramMediaLocalConsolidator):
    await input_product_field(msg, fsm_storage, input_product_manager, state, msg.text, media_consolidator)


@router.message(StateFilter(AddProductStates.add_price, EditProductStates.EditParam.edit_price))
async def add_price_handler(msg: Message, state: FSMContext, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                    media_consolidator: TelegramMediaLocalConsolidator):
    await add_price(msg, fsm_storage, input_product_manager, state, media_consolidator)