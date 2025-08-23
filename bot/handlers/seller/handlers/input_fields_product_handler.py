from bot.handlers.handlers_import import *

from aiogram import F
from aiogram.filters import StateFilter, or_f, and_f

from ..helpers import *
from bot.handlers.utils import create_menu_catalog
from bot.handlers.seller.templates.messages import *
from bot.handlers.seller.templates.fsm_states import *
from bot.handlers.seller.templates.configs import BASE_STATE

from bot.handlers.utils import repack_choice_catalog_data
from bot.constants.callback import PASS_CALLBACK
from bot.constants.redis_keys import UserSessionKeys, FSMKeys
from bot.configs.constants import UserTypes
from bot.utils.message_utils.message_utils import *
from bot.utils.exception import UnknownCallback
from bot.utils.message_utils.keyboard_utils import *
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.utils.message_utils.media_messages_utils import input_media_album
from bot.utils.cache_utils.cache_utils import caching_media

from bot.services.product.services import ProductService


router = Router()


@router.callback_query(CallbackFilter(scope='product', subscope='add'), TypeUserFilter(UserTypes.SELLER))
async def process_product_actions(cb: CallbackQuery, state: FSMContext, session: UserSession,
                                  product_service: ProductService):
    _, subscope, action = parse_callback(cb.data)
    new_message: MessageSetting | None; is_send_new: bool
    new_message, is_send_new = None, True

    if action == 'start':
        now_state: str = await state.get_state()
        if not now_state.startswith(EditProductStates.group_name):
            await state.set_state(AddProductStates.choose_catalog)

        new_message = await create_menu_catalog(state, create_callback('product',
                                                                       subscope,
                                                                       'choice_catalog'),
                                                product_service)

    elif action.startswith('choice_catalog'):
        selected_catalog = await repack_choice_catalog_data(state, cb.data)
        await handler_input_product_field(cb.message, session, state, 'catalog',
                                          selected_catalog, is_delete_user_message=False)

    elif action == 'send_product':
        await send_message(session, cb.bot, MessageSetting(text='ожидайте', keyboard=create_callback_inline_keyboard(
            InlineButtonSetting(
                text='ok', callback=PASS_CALLBACK
            ))))
        await state.set_state(BASE_STATE)
    else:
        raise UnknownCallback(cb.data)

    if new_message is not None:
        await send_message(session, cb.bot, new_message, is_send_new)


@router.message(StateFilter(AddProductStates.add_name, EditProductStates.EditParam.edit_name))
async def add_name(msg: Message, state: FSMContext, session: UserSession):
    await handler_input_product_field(msg, session, state, 'name', msg.text)


@router.message(StateFilter(AddProductStates.add_description,
                                   EditProductStates.EditParam.edit_description))
async def add_description(msg: Message, state: FSMContext, session: UserSession):
    await handler_input_product_field(msg, session, state, 'description', msg.text)


@router.message(or_f(F.photo,
                     F.video,
                     Command('skip'),
                     StateFilter(AddProductStates.add_photo, EditProductStates.EditParam.edit_photo)))
async def add_photo(msg: Message, state: FSMContext, session: UserSession):
    album = await input_media_album(msg.bot, state, msg, PROCESS_INPUT_PHOTO_PRODUCT_MESSAGE, PHOTO_INPUT_STOP_TEXT)
    is_skip = msg.text == SKIP_INPUT_PHOTO_COMMAND
    if album or is_skip:
        user_data = None
        if not is_skip:
            user_data = await caching_media(album, msg.bot)
        await handler_input_product_field(msg, session, state, 'media', user_data, False)


@router.message(StateFilter(AddProductStates.add_price, EditProductStates.EditParam.edit_price))
async def add_price(msg: Message, state: FSMContext, session: UserSession):
    await handler_input_product_field(msg, session, state, 'price', msg.text)