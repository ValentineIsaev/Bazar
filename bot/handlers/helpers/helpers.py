from asyncio import Lock

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, inline_keyboard_markup
from aiogram.fsm.state import State

from .messages import HELLO_TEXT_MSG_WITH_NAME, HELLO_TEXT_MSG
from .keyboards import MEDIATOR_CHAT_BUTTON_TEXT, MEDIATOR_CHATS_CALLBACK

from bot.constants.redis_keys import StorageKeys
from bot.constants.user_constants import TypesUser

from bot.utils.message_utils import (send_message, delete_bot_message, delete_media_message,
                                     get_callback_inline_keyboard)

from bot.types.storage import FSMStorage, LocalObjPath, TelegramMediaLocalConsolidator
from bot.types.utils import MessageSetting, CallbackSetting, InlineButtonSetting

from bot.managers.mediator_manager import MediatorManager
from bot.managers.product_managers import ProductCategoryManager
from bot.managers.catalog_manager import CatalogManager
from bot.components.catalog_renderer import CategoryCatalogRenderer, MEDIATOR_COUNT_BUTTON


def get_hello_text_msg(user_name: str) -> str:
        if len(user_name) > 1 and user_name.strip():
            return HELLO_TEXT_MSG_WITH_NAME.insert((user_name,))
        return HELLO_TEXT_MSG.insert(())


async def get_menu_keyboard(*button_settings: InlineButtonSetting,
                            mediator_manager: MediatorManager[MessageSetting],
                            user_id: int, user_role: TypesUser) -> inline_keyboard_markup:
    count_new_mediator_msgs = await mediator_manager.get_count_all_new_msgs(user_id, user_role)
    text = MEDIATOR_CHAT_BUTTON_TEXT + MEDIATOR_COUNT_BUTTON.insert((count_new_mediator_msgs,)) \
        if count_new_mediator_msgs > 0 else MEDIATOR_CHAT_BUTTON_TEXT
    mediator_button_setting = InlineButtonSetting(text=text,
                                                  callback=MEDIATOR_CHATS_CALLBACK)
    return get_callback_inline_keyboard(mediator_button_setting, *button_settings)


async def processing_start(fsm_storage: FSMStorage, msg: Message, start_msg: MessageSetting,
                           state: FSMContext=None,new_type_user: TypesUser=None,
                           fsm_data: dict=None, new_state: State=None, is_delete_msg: bool=True):
    if is_delete_msg:
        await msg.delete()
    user_data = await fsm_storage.get_all_data()
    if not user_data:
        user_data = {StorageKeys.CHAT_ID: msg.chat.id,
                     StorageKeys.USERNAME: msg.from_user.first_name,
                     }
        await fsm_storage.update_data(**user_data)
    else:
        await delete_bot_message(fsm_storage, msg.bot)
        await delete_media_message(fsm_storage, msg.bot)

    if new_type_user is not None:
        if fsm_data is None:
            fsm_data = {StorageKeys.USERTYPE: new_type_user}
        else:
            fsm_data[StorageKeys.USERTYPE] = new_type_user
    if fsm_data is not None: await fsm_storage.update_data(**fsm_data)
    if new_state is not None: await state.set_state(new_state)

    await send_message(fsm_storage, msg.bot, start_msg)


async def set_category_catalog_manager(catalog_manager: CatalogManager,
                                       products_catalog_manager: ProductCategoryManager,
                                       callback_prefix: CallbackSetting):
    category_catalog = await products_catalog_manager.get_category_products()

    await catalog_manager.set_catalog_service(category_catalog)
    await catalog_manager.set_renderer(CategoryCatalogRenderer(callback_prefix))


# global_lock = Lock()
# async def get_media_objs(msg: Message, fsm_storage: FSMStorage, media_consolidator: TelegramMediaLocalConsolidator,
#                          stop_input_text: str, reply_answer_msg: MessageSetting,
#                          skip_command: str=None, len_: int=3) -> tuple[LocalObjPath, ...]:
#     result = ()
#     async with global_lock:
#         user_lock = await fsm_storage.get_value(StorageKeys.USER_ASYNC_LOCK)
#         if user_lock is None:
#             user_lock = Lock()
#             await fsm_storage.update_value(StorageKeys.USER_ASYNC_LOCK, user_lock)
#
#     async with user_lock:
#         temp_bots_msg_id, media_msgs_id, saved_media_data = await fsm_storage.get_data(StorageKeys.TEMP_BOT_MSG,
#                                                                                        StorageKeys.USERS_MEDIA_MSGS,
#                                                                                        StorageKeys.SAVED_MEDIA_DATA)
#
#         is_over = True if saved_media_data is not None and len(saved_media_data) == len_-1 else False
#         if msg.text != stop_input_text and msg.text != skip_command and not is_over:
#             saved_data = get_saved_media_data(msg)
#
#             if saved_media_data is None:
#                 saved_media_data = []
#             saved_media_data.append(saved_data)
#
#             if media_msgs_id is None:
#                 media_msgs_id = []
#             media_msgs_id.append(msg.message_id)
#
#             if temp_bots_msg_id is not None:
#                 await msg.bot.delete_message(msg.chat.id, temp_bots_msg_id)
#
#             sent_msg = await msg.answer(text=reply_answer_msg.text, reply_markup=reply_answer_msg.keyboard)
#             temp_bots_msg_id = sent_msg.message_id
#
#         else:
#             if is_over:
#                 saved_data = get_saved_media_data(msg)
#                 if saved_data is not None:
#                     saved_media_data.append(saved_data)
#
#             if temp_bots_msg_id is not None:
#                 await msg.bot.delete_message(msg.chat.id, temp_bots_msg_id)
#                 temp_bots_msg_id = None
#
#             if media_msgs_id is not None:
#                 for media_msg_id in media_msgs_id:
#                     await msg.bot.delete_message(msg.chat.id, media_msg_id)
#
#                 media_msgs_id = None
#
#             if saved_media_data is not None:
#                 result = await media_consolidator.save_temp_obj(*saved_media_data)
#                 saved_media_data = None
#
#         await fsm_storage.update_data(**{StorageKeys.TEMP_BOT_MSG: temp_bots_msg_id,
#                                          StorageKeys.USERS_MEDIA_MSGS: media_msgs_id,
#                                          StorageKeys.SAVED_MEDIA_DATA: saved_media_data})
#         return result
