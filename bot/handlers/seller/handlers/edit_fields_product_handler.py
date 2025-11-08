from bot.handlers.seller.templates.messages import EDIT_PRODUCT_MESSAGE
from bot.handlers.seller.templates.fsm import EditProductStates
from aiogram import Router

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from bot.managers.catalog_manager import CatalogManager
from bot.managers.product_managers import InputProductManager, ProductCategoryCatalogManager
from bot.storage.local_media_data import TelegramMediaLocalConsolidator
from bot.utils.message_utils.message_utils import MessageSetting, send_message
from bot.handlers.seller.templates.configs import FieldConfig
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.configs.constants import UserTypes
from bot.types.utils import CallbackSetting

from bot.storage.redis import FSMStorage

from .input_fields_product_handler import (add_catalog, add_media, add_price, add_name,
                                           add_description)
from bot.handlers.utils import render_product_message
from ..templates.keyboards import ADD_PRODUCT_COMPLETE_KEYBOARD
from ..templates.fsm import AddProductStates, EDIT_PRODUCT_MESSAGES

router = Router()


@router.callback_query(CallbackFilter('product','edit'),
                              TypeUserFilter(UserTypes.SELLER))
async def edit_product_handler(cb: CallbackQuery, state: FSMContext, fsm_storage: FSMStorage,
                               input_product_manager: InputProductManager, catalog_manager: CatalogManager,
                               product_category_catalog_manager: ProductCategoryCatalogManager,
                               media_consolidator: TelegramMediaLocalConsolidator):
    _, _, action = CallbackSetting.decode_callback(cb.data)

    new_msg: MessageSetting | None = None
    new_state: State
    if action == 'start':
        new_state = EditProductStates.choose_param
        new_msg = EDIT_PRODUCT_MESSAGES
        await send_message(fsm_storage, cb.bot, EDIT_PRODUCT_MESSAGE)

    elif action == 'catalog':
        new_state = EditProductStates.EditParam.edit_catalog
        await state.set_state(new_state)

        callback_cls_data = cb.__dict__.copy()
        callback_cls_data['data'] = CallbackSetting.encode_callback('product',
                                                                    'add_catalog',
                                                                    'start')
        new_cb = cb.__class__(**callback_cls_data)
        await add_catalog(new_cb, cb.bot, state, fsm_storage, input_product_manager, catalog_manager,
                          product_category_catalog_manager, media_consolidator)

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
        await send_message(fsm_storage, cb.bot, new_msg)
