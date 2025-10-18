from aiogram.fsm.state import State
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.handlers.seller.templates.messages import *
from bot.handlers.seller.templates.configs import FieldConfig, ADD_FIELD_PRODUCT_CONFIGS
from bot.handlers.seller.templates.fsm_states import AddProductStates
from bot.storage.redis import Storage

from bot.managers.product_managers import ProductManager

from bot.handlers.seller.templates.fsm_states import EditProductStates
from bot.utils.helper import get_data_state
from bot.constants.redis_keys import UserSessionKeys, FSMKeys
from bot.services.product.dto import Product
from bot.services.product.services import InputProductService
from bot.utils.message_utils.message_utils import MessageSetting, send_message, delete_bot_message
from bot.utils.message_utils.media_messages_utils import send_media_message, send_cached_media_message


async def handler_input_product_field(msg: Message, storage: Storage, product_manager: ProductManager, state: FSMContext,
                                      field_name: str, value, is_delete_user_message: bool=True):
    if is_delete_user_message:
        await msg.delete()

    # product_service: InputProductService = await state.get_value(FSMKeys.SellerKeys.ADD_PRODUCT_MANAGER)
    # if product_service is None:
    #     product_service = InputProductService(Product())
    #     await state.update_data(**{FSMKeys.SellerKeys.ADD_PRODUCT_MANAGER: product_service})

    filed_config: FieldConfig = ADD_FIELD_PRODUCT_CONFIGS[field_name]
    result = await product_manager.add_value_product(field_name, value)
    # result = product_service.add_value(field_name, value)

    new_message: MessageSetting | None = None
    if result is None:
        # await state.update_data(**{FSMKeys.SellerKeys.ADD_PRODUCT_MANAGER: product_service})
        now_state: str = await state.get_state()
        next_state: State | None = None
        if now_state.startswith(EditProductStates.group_name) or filed_config.is_end_field:
            new_message, next_state = await complete_product(product_manager)
        elif now_state.startswith(AddProductStates.group_name):
            next_config: FieldConfig = ADD_FIELD_PRODUCT_CONFIGS[filed_config.next_field]
            new_message, next_state = next_config.input_msg, filed_config.next_state
        else:
            ValueError(f'Wrong state: {state}')
        await state.set_state(next_state)
    else:
        new_message = result

    if new_message is not None:
        await send_message(storage, msg.bot, new_message, False)


async def complete_product(product_manager: ProductManager) -> tuple[None | MessageSetting, State]:
    # product_service: InputProductService = await state.get_value(FSMKeys.SellerKeys.ADD_PRODUCT_MANAGER)
    # new_message = None
    product = product_manager.product
    product_data = (product.name,
                    product.catalog,
                    product.description,
                    product.price)
    complete_text = ADD_PRODUCT_FORM_TEXT.insert(product_data)
    # if product.media is not None:
    #     # await delete_bot_message(session)
    #     product_message = MessageSetting(text=complete_text,
    #                                      cache_media=product.media.get_cache())
    #     # await send_cached_media_message(session, bot, product_message)
    #     await send_message(session, bot, COMPLETE_ADD_PRODUCT_MESSAGE_WITH_MEDIA)
    # else:
    return (MessageSetting(text=COMPLETE_ADD_PRODUCT_MESSAGE.insert((complete_text,)),
                                 keyboard=ADD_PRODUCT_COMPLETE_KEYBOARD,
                                 cache_media=product.media.get_cache()),
            AddProductStates.user_checking)
