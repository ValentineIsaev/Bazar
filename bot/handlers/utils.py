from asyncio import Lock
from typing import Any, Callable

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.storage.redis.storage import FSMStorage
from aiogram.fsm.state import State

from bot.constants.redis_keys import FSMKeys, UserSessionKeys

from bot.types.utils import MessageSetting
from bot.utils.message_utils import send_message, get_saved_media_data, delete_bot_message, delete_media_message

from bot.managers.product_managers import ProductCategoryCatalogManager, InputProductManager
from bot.managers.catalog_manager import CatalogManager

from bot.components.catalog_renderer import CategoryCatalogRenderer
from bot.types.utils import CallbackSetting

from bot.storage.local_media_data import LocalObjPath, TelegramMediaLocalConsolidator
from bot.services.product import Product
from aiogram.types import inline_keyboard_markup
from .utils_temp import PRODUCT_TEXT, INVALID_PRICE
from ..utils.message_utils.config_obj import MediaSetting


invalidate_msgs = {
    InputProductManager.VALIDATE_ERRORS.INVALID_PRICE: INVALID_PRICE
}
def render_invalidate_input_product_msg(error: InputProductManager.VALIDATE_ERRORS, value: Any) -> MessageSetting:
    return MessageSetting(text=invalidate_msgs.get(error).insert((value,)))


async def user_start_handler(bot: Bot, fsm_storage: FSMStorage, state: FSMContext, base_state: State, user_type: str,
                             start_message: MessageSetting):
    if await state.get_state() != base_state:
        await state.set_state(base_state)

    now_type_user = await fsm_storage.get_value(FSMKeys.USERTYPE)
    if now_type_user != user_type:
        await state.update_data({FSMKeys.USERTYPE: user_type})

    await send_message(fsm_storage, bot, start_message)


async def set_category_catalog_manager(catalog_manager: CatalogManager,
                                       products_catalog_manager: ProductCategoryCatalogManager,
                                       callback_prefix: CallbackSetting):
    category_catalog = await products_catalog_manager.get_category_products()

    await catalog_manager.set_catalog_service(category_catalog)
    await catalog_manager.set_renderer(CategoryCatalogRenderer(callback_prefix))


global_lock = Lock()
async def get_media_objs(msg: Message, fsm_storage: FSMStorage, media_consolidator: TelegramMediaLocalConsolidator,
                         stop_input_text: str, reply_answer_msg: MessageSetting,
                         skip_command: str=None, len_: int=3) -> tuple[LocalObjPath, ...]:
    result = ()
    async with global_lock:
        user_lock = await fsm_storage.get_value(FSMKeys.USER_ASYNC_LOCK)
        if user_lock is None:
            user_lock = Lock()
            await fsm_storage.update_value(FSMKeys.USER_ASYNC_LOCK, user_lock)

    async with user_lock:
        temp_bots_msg_id, media_msgs_id, saved_media_data = await fsm_storage.get_data(FSMKeys.TEMP_BOT_MSG,
                                                                                       FSMKeys.USERS_MEDIA_MSGS,
                                                                                       FSMKeys.SAVED_MEDIA_DATA)

        is_over = True if saved_media_data is not None and len(saved_media_data) == len_-1 else False
        if msg.text != stop_input_text and msg.text != skip_command and not is_over:
            saved_data = get_saved_media_data(msg)

            if saved_media_data is None:
                saved_media_data = []
            saved_media_data.append(saved_data)

            if media_msgs_id is None:
                media_msgs_id = []
            media_msgs_id.append(msg.message_id)

            if temp_bots_msg_id is not None:
                await msg.bot.delete_message(msg.chat.id, temp_bots_msg_id)

            sent_msg = await msg.answer(text=reply_answer_msg.text, reply_markup=reply_answer_msg.keyboard)
            temp_bots_msg_id = sent_msg.message_id

        else:
            if is_over:
                saved_data = get_saved_media_data(msg)
                if saved_data is not None:
                    saved_media_data.append(saved_data)

            if temp_bots_msg_id is not None:
                await msg.bot.delete_message(msg.chat.id, temp_bots_msg_id)
                temp_bots_msg_id = None

            if media_msgs_id is not None:
                for media_msg_id in media_msgs_id:
                    await msg.bot.delete_message(msg.chat.id, media_msg_id)

                media_msgs_id = None

            if saved_media_data is not None:
                result = await media_consolidator.save_temp_obj(*saved_media_data)
                saved_media_data = None

        await fsm_storage.update_data(**{FSMKeys.TEMP_BOT_MSG: temp_bots_msg_id,
                                         FSMKeys.USERS_MEDIA_MSGS: media_msgs_id,
                                         FSMKeys.SAVED_MEDIA_DATA: saved_media_data})
        return result

def render_product_message(product: Product, media_consolidator: TelegramMediaLocalConsolidator,
                           keyboard: inline_keyboard_markup=None) -> MessageSetting:
    return MessageSetting(
        text=PRODUCT_TEXT.insert((product.catalog, product.name_product, product.description, product.price)),
        keyboard=keyboard,
        media=tuple(MediaSetting(type_media=media.type_media, path=media.path)
                       for media in media_consolidator.get_obj_data(*product.media_path)) \
        if product.media_path is not None else None
    )

async def delete_product_message(fsm_storage: FSMStorage, bot: Bot):
    bot_msg, bot_media_msg, product_msg, product_media_msg = await fsm_storage.get_data(UserSessionKeys.BOTS_MESSAGE_ID,
                                                                                        UserSessionKeys.BOTS_MEDIA_MESSAGE_ID,
                                                                                        UserSessionKeys.PRODUCT_MESSAGE_ID,
                                                                                        UserSessionKeys.PRODUCT_MEDIA_MESSAGE_ID)
    if product_msg is not None or product_media_msg is not None:
        await fsm_storage.update_data(**{UserSessionKeys.BOTS_MESSAGE_ID: product_msg,
                                         UserSessionKeys.BOTS_MEDIA_MESSAGE_ID: product_media_msg})

        await delete_bot_message(fsm_storage, bot)
        await delete_media_message(fsm_storage, bot)

        await fsm_storage.update_data(**{UserSessionKeys.BOTS_MESSAGE_ID: bot_msg,
                                         UserSessionKeys.BOTS_MEDIA_MESSAGE_ID: bot_media_msg,
                                         UserSessionKeys.PRODUCT_MESSAGE_ID: None,
                                         UserSessionKeys.PRODUCT_MEDIA_MESSAGE_ID: None})
