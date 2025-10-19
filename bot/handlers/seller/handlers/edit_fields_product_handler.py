from bot.handlers.seller.templates.messages import EDIT_PRODUCT_MESSAGE
from bot.handlers.seller.templates.fsm_states import EditProductStates, EDIT_PARAM_PRODUCT_STATES
from aiogram import Router

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.utils.message_utils.message_utils import MessageSetting, send_message
from bot.handlers.seller.templates.configs import FieldConfig, ADD_FIELD_PRODUCT_CONFIGS
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.configs.constants import UserTypes
from bot.utils.message_utils.keyboard_utils import parse_callback

from bot.storage.redis import FSMStorage

router = Router()


@router.callback_query(CallbackFilter('product','edit_product'),
                              TypeUserFilter(UserTypes.SELLER))
async def edit_product_handler(cb: CallbackQuery, state: FSMContext, fsm_storage: FSMStorage):
    _, _, action = parse_callback(cb.data)
    new_message: MessageSetting
    is_send_new = True
    if action == 'start':
        new_message, is_send_new = EDIT_PRODUCT_MESSAGE, False
        await state.set_state(EditProductStates.choose_param)
    else:
        field_config: FieldConfig = ADD_FIELD_PRODUCT_CONFIGS.get(action)
        if field_config is None:
            raise ValueError(f'Wrong field name: {action}')
        new_message = field_config.input_msg
        new_state = EDIT_PARAM_PRODUCT_STATES.get(action)
        await state.set_state(new_state)

    await send_message(fsm_storage, cb.bot, new_message, is_send_new)