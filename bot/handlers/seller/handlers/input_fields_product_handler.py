from bot.handlers.handlers_import import *

from aiogram import F
from aiogram.filters import StateFilter, or_f

from ..helpers import *
from bot.handlers.seller.templates.fsm_states import *
from bot.handlers.seller.templates.messages import *
from bot.handlers.seller.templates.configs import BASE_STATE

from bot.handlers.common.catalog import create_catalog_message
from bot.configs.constants import UserTypes, PASS_CALLBACK
from bot.utils.message_utils.message_utils import *
from bot.utils.exception import UnknownCallback
from bot.utils.helper import get_data_state
from bot.utils.message_utils.keyboard_utils import *
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.utils.message_utils.media_messages_utils import make_cache_media_operator, input_media_album
from bot.services.product.services import ProductService
from bot.services.product.models import CatalogMenu
from bot.services.product.models import InputProduct


router = Router()


@router.callback_query(CallbackFilter(scope='product', subscope='add'), TypeUserFilter(UserTypes.SELLER))
async def process_product_actions(cb: CallbackQuery, state: FSMContext):
    _, subscope, action = parse_callback(cb.data)
    new_message: MessageSetting | None; is_send_new: bool
    new_message, is_send_new = None, True

    if action == 'start':
        now_state: str = await state.get_state()
        if not now_state.startswith(EditProductStates.group_name):
            await state.set_state(AddProductStates.choose_catalog)
            product_form = InputProduct()
            await state.update_data(**{ParamFSM.SellerData.ADD_PRODUCT_OPERATOR: product_form})

        catalog_menu = ProductService.get_product_catalog()
        await state.update_data(**{ParamFSM.ProductData.CATALOG_MENU: catalog_menu,
                                       ParamFSM.ProductData.CATALOG_MENU_CALLBACK: create_callback('product',
                                                                                       subscope,
                                                                                       'choice_catalog')})

        new_message = await create_catalog_message(state)

    elif action.startswith('choice_catalog'):
        catalog_menu: CatalogMenu
        (catalog_menu,) = await get_data_state(state, ParamFSM.ProductData.CATALOG_MENU)

        number_catalog = int(action.replace('choice_catalog-', ''))

        selected_catalog = catalog_menu.get_catalogs()[number_catalog]
        await handler_input_product_field(cb.message, state, 'catalog',
                                          selected_catalog, is_delete_user_message=False)

    elif action == 'send_product':
        await send_message(state, cb.bot, MessageSetting(text='ожидайте', keyboard=create_callback_inline_keyboard(
            InlineButtonSetting(
                text='ok', callback=PASS_CALLBACK
            ))))
        await state.set_state(BASE_STATE)
    else:
        raise UnknownCallback(cb.data)

    if new_message is not None:
        await send_message(state, cb.bot, new_message, is_send_new)


@router.message(StateFilter(AddProductStates.add_name, EditProductStates.EditParam.edit_name))
async def add_name(msg: Message, state: FSMContext):
    await handler_input_product_field(msg, state, 'name', msg.text)


@router.message(StateFilter(AddProductStates.add_description,
                                   EditProductStates.EditParam.edit_description))
async def add_description(msg: Message, state: FSMContext):
    await handler_input_product_field(msg, state, 'description', msg.text)


@router.message(StateFilter(AddProductStates.add_photo, EditProductStates.EditParam.edit_photo),
                or_f(F.photo,
                     F.video,
                     F.media_group_id,
                     Command('skip')))
async def add_photo(msg: Message, state: FSMContext):
    # album = await input_media_album(state, msg, '/skip', PROCESS_INPUT_PHOTO_PRODUCT_MESSAGE)
    # if album is not None:
    #     user_data = await make_cache_media_operator(msg, msg.bot)
    #     await handler_input_product_field(msg, state, 'photo', user_data)
    await state.set_state(AddProductStates.add_price)


@router.message(StateFilter(AddProductStates.add_price, EditProductStates.EditParam.edit_price))
async def add_price(msg: Message, state: FSMContext):
    await handler_input_product_field(msg, state, 'price', msg.text)