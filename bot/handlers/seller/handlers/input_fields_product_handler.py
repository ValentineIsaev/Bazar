from  asyncio.locks import Lock

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram import F
from aiogram.filters import StateFilter, or_f, and_f

from bot.handlers.seller.templates.messages import *
from bot.handlers.seller.templates.fsm_states import *
from bot.handlers.seller.templates.configs import BASE_STATE
from bot.handlers.utils import set_category_catalog_manager
from bot.constants.callback import PASS_CALLBACK
from bot.constants.redis_keys import UserSessionKeys, FSMKeys
from bot.configs.constants import UserTypes
from bot.utils.message_utils import *
from bot.utils.exception import UnknownCallback
from bot.utils.message_utils.keyboard_utils import *
from bot.utils.filters import CallbackFilter, TypeUserFilter
from bot.utils.message_utils.media_messages_utils import input_media_album

from bot.storage.redis import FSMStorage
from bot.managers.product_managers import InputProductManager, ProductCategoryCatalogManager
from bot.managers.catalog_manager import CatalogManager
from bot.types.utils import CallbackSetting

from bot.types.storage import TelegramMediaLocalConsolidator
from ..templates.configs import *


router = Router()

async def handler_input_product_field(msg: Message, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                                      state: FSMContext, field_name: str, value, is_delete_user_message: bool=True):
    if is_delete_user_message:
        await msg.delete()

    filed_config: FieldConfig = ADD_FIELD_PRODUCT_CONFIGS[field_name]
    result = await input_product_manager.add_value(field_name, value)
    new_message: MessageSetting | None = None
    if result is None:
        now_state: str = await state.get_state()
        next_state: State | None = None
        if now_state.startswith(EditProductStates.group_name) or filed_config.is_end_field:
            new_message, next_state = await complete_product(input_product_manager)
        elif now_state.startswith(AddProductStates.group_name):
            next_config: FieldConfig = ADD_FIELD_PRODUCT_CONFIGS[filed_config.next_field]
            new_message, next_state = next_config.input_msg, filed_config.next_state
        else:
            ValueError(f'Wrong state: {state}')
        await state.set_state(next_state)
    else:
        new_message = result

    if new_message is not None:
        await send_message(fsm_storage, msg.bot, new_message, False)


async def complete_product(input_product_manager: InputProductManager) -> tuple[None | MessageSetting, State]:
    product = await input_product_manager.get_product()
    product_data = (product.name,
                    product.catalog,
                    product.description,
                    product.price)
    complete_text = ADD_PRODUCT_FORM_TEXT.insert(product_data)
    return (MessageSetting(text=COMPLETE_ADD_PRODUCT_MESSAGE.insert((complete_text,)),
                                 keyboard=ADD_PRODUCT_COMPLETE_KEYBOARD,
                                 cache_media=product.media.get_cache()),
            AddProductStates.user_checking)

@router.callback_query(CallbackFilter(scope='product', subscope='add'), TypeUserFilter(UserTypes.SELLER))
async def add_product_actions(cb: CallbackQuery, state: FSMContext, fsm_storage: FSMStorage,
                              input_product_manager: InputProductManager, catalog_manager: CatalogManager,
                              product_category_catalog_manager: ProductCategoryCatalogManager):
    scope, subscope, action = CallbackSetting.decode_callback(cb.data)
    new_message: MessageSetting | None; is_send_new: bool
    new_message, is_send_new = None, True

    if action == 'start':
        now_state: str = await state.get_state()
        if not now_state.startswith(EditProductStates.group_name):
            await input_product_manager.new()
            await state.set_state(AddProductStates.choose_catalog)

        await set_category_catalog_manager(catalog_manager, product_category_catalog_manager,
                                           CallbackSetting(scope,
                                                           subscope,
                                                           'choice_catalog'))
        new_message = await catalog_manager.render_message()

    elif action.startswith('choice_catalog'):
        selected_catalog = await catalog_manager.get_catalog_by_callback(cb.data)
        await handler_input_product_field(cb.message, fsm_storage, input_product_manager, state, 'catalog',
                                          selected_catalog, is_delete_user_message=False)

    elif action == 'send_product':
        await send_message(fsm_storage, cb.bot, MessageSetting(text='ожидайте', keyboard=get_callback_inline_keyboard(
            InlineButtonSetting(
                text='ok', callback=PASS_CALLBACK
            ))))
        await state.set_state(BASE_STATE)
    else:
        raise UnknownCallback(cb.data)

    if new_message is not None:
        await send_message(fsm_storage, cb.bot, new_message, is_send_new)


@router.message(StateFilter(AddProductStates.add_name, EditProductStates.EditParam.edit_name))
async def add_name(msg: Message, state: FSMContext, fsm_storage: FSMStorage, input_product_manager: InputProductManager):
    await handler_input_product_field(msg, fsm_storage, input_product_manager, state, 'name_product', msg.text)


@router.message(StateFilter(AddProductStates.add_description,
                                   EditProductStates.EditParam.edit_description))
async def add_description(msg: Message, state: FSMContext, fsm_storage: FSMStorage, input_product_manager: InputProductManager):
    await handler_input_product_field(msg, fsm_storage, input_product_manager, state, 'description', msg.text)


# @router.message(or_f(F.photo,
#                      F.video,
#                      Command('skip'),
#                      StateFilter(AddProductStates.add_photo, EditProductStates.EditParam.edit_photo)))
async def add_photo(msg: Message, state: FSMContext, fsm_storage: FSMStorage, input_product_manager: InputProductManager,
                    media_consolidator: TelegramMediaLocalConsolidator):
    album = await input_media_album(msg.bot, state, msg, PROCESS_INPUT_PHOTO_PRODUCT_MESSAGE, PHOTO_INPUT_STOP_TEXT)
    is_skip = msg.text == SKIP_INPUT_PHOTO_COMMAND
    if album or is_skip:
        user_data = None
        if not is_skip:
            user_data = await media_consolidator.save_temp_obj(*album)
        await handler_input_product_field(msg, fsm_storage, input_product_manager, state, 'media_path', user_data, False)


global_lock = Lock()
@router.message(or_f(F.photo, F.video, Command('skip'),
                     StateFilter(AddProductStates.add_photo,
                                        EditProductStates.EditParam.edit_photo)))
async def add_media(msg: Message, state: FSMContext, fsm_storage: FSMStorage,
                    input_product_manager: InputProductManager,
                    media_consolidator: TelegramMediaLocalConsolidator):
    CAPACITY = 3
    async with global_lock:
        lock = await fsm_storage.get_value(FSMKeys.USER_ASYNC_LOCK)
        if lock is None:
            lock = Lock()
            await fsm_storage.update_value(FSMKeys.USER_ASYNC_LOCK, lock)

    async with lock:
        temp_bots_msg, media_msgs, saved_media_data = await fsm_storage.get_data(FSMKeys.TEMP_BOT_MSG,
                                                          FSMKeys.USERS_MEDIA_MSGS, FSMKeys.SAVED_MEDIA_DATA)
    is_over = True if saved_media_data is not None and len(saved_media_data) == CAPACITY-1 else False

    if (msg.text != PHOTO_INPUT_STOP_TEXT or msg.text != '/skip') and not is_over:
        (obj,) = await media_consolidator.save_temp_obj(get_saved_media_data(msg))
        async with lock:
            if saved_media_data is None:
                saved_media_data = []
            saved_media_data.append(obj)

            if media_msgs is None:
                media_msgs = []
            media_msgs.append(msg.message_id)

        if temp_bots_msg is not None:
            await msg.bot.delete_message(msg.chat.id, temp_bots_msg)

        temp_bots_msg = await send_message(fsm_storage, msg.bot,
                                           PROCESS_INPUT_PHOTO_PRODUCT_MESSAGE)

    else:
        async with lock:
            if is_over:
                (obj,) = await media_consolidator.save_temp_obj(get_saved_media_data(msg))
                saved_media_data.append(obj)

            if temp_bots_msg is not None:
                await msg.bot.delete_message(msg.chat.id, temp_bots_msg)
                temp_bots_msg = None

            if media_msgs is not None:
                for media_msg in media_msgs:
                    await msg.bot.delete_message(msg.chat.id, media_msg.message_id)

                media_msgs = None

            await handler_input_product_field(msg, fsm_storage, input_product_manager, state,
                                              'media_path', saved_media_data)
            saved_media_data = None

        await fsm_storage.update_data(**{FSMKeys.TEMP_BOT_MSG: temp_bots_msg,
                                     FSMKeys.USERS_MEDIA_MSGS: media_msgs,
                                     FSMKeys.SAVED_MEDIA_DATA: saved_media_data})


@router.message(StateFilter(AddProductStates.add_price, EditProductStates.EditParam.edit_price))
async def add_price(msg: Message, state: FSMContext, fsm_storage: FSMStorage, input_product_manager: InputProductManager):
    await handler_input_product_field(msg, fsm_storage, input_product_manager, state, 'price', msg.text)