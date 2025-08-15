from aiogram.fsm.state import State
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.handlers.seller.templates.messages import *
from bot.handlers.seller.templates.configs import FieldConfig, ADD_FIELD_PRODUCT_CONFIGS
from bot.handlers.seller.templates.fsm_states import AddProductStates

from bot.handlers.seller.templates.fsm_states import EditProductStates
from bot.utils.helper import get_data_state
from bot.configs.constants import ParamFSM
from bot.services.product.models import InputProduct
from bot.utils.message_utils.message_utils import MessageSetting, send_message, delete_bot_message
from bot.utils.message_utils.media_messages_utils import send_media_message, send_cached_media_message


async def handler_input_product_field(msg: Message, state: FSMContext, field_name: str, value,
                                      is_delete_user_message: bool=True):
    if is_delete_user_message:
        await msg.delete()

    product: InputProduct = await state.get_value(ParamFSM.SellerData.ADD_PRODUCT_OPERATOR)
    if product is None:
        product = InputProduct()
        await state.update_data(**{ParamFSM.SellerData.ADD_PRODUCT_OPERATOR: product})

    filed_config: FieldConfig = ADD_FIELD_PRODUCT_CONFIGS[field_name]
    result = product.add_value(field_name, value)

    new_message: MessageSetting | None = None
    if result is None:
        await state.update_data(**{ParamFSM.SellerData.ADD_PRODUCT_OPERATOR: product})
        now_state: str = await state.get_state()
        next_state: State | None = None
        if now_state.startswith(EditProductStates.group_name) or filed_config.is_end_field:
            new_message, next_state = await complete_product(state, msg.bot)
        elif now_state.startswith(AddProductStates.group_name):
            next_config: FieldConfig = ADD_FIELD_PRODUCT_CONFIGS[filed_config.next_field]
            new_message, next_state = next_config.input_msg, filed_config.next_state
        else:
            ValueError(f'Wrong state: {now_state}')
        await state.set_state(next_state)
    else:
        new_message = result

    if new_message is not None:
        await send_message(state, msg.bot, new_message, False)


async def complete_product(state: FSMContext, bot: Bot) -> tuple[None, State]:
    product: InputProduct
    (product, chat_id) = await get_data_state(state, ParamFSM.SellerData.ADD_PRODUCT_OPERATOR,
                                                       ParamFSM.BotMessagesData.CHAT_ID)

    new_message = None
    product_data = (product.name,
                    product.catalog,
                    product.description,
                    product.price)
    complete_text = ADD_PRODUCT_FORM_TEXT.insert(product_data)
    if product.media is not None:
        await delete_bot_message(state, bot)
        product_message = MessageSetting(text=complete_text,
                                         cache_media=product.media.get_cache())
        await send_cached_media_message(state, bot, product_message)
        await send_message(state, bot, COMPLETE_ADD_PRODUCT_MESSAGE_WITH_MEDIA)
    else:
        new_message = MessageSetting(text=COMPLETE_ADD_PRODUCT_MESSAGE.insert((complete_text,)),
                                     keyboard=ADD_PRODUCT_COMPLETE_KEYBOARD)

    return new_message, AddProductStates.user_checking
