import math

from aiogram import Bot

from .config_obj import MessageSetting
from .media_messages_utils import send_media_message

from bot.constants.redis_keys import UserSessionKeys
from bot.storage.redis import FSMStorage


async def delete_bot_message(fsm_storage: FSMStorage, bot: Bot) -> None:
    bot_message_id, chat_id = await fsm_storage.get_data(UserSessionKeys.BOTS_MESSAGE_ID, UserSessionKeys.CHAT_ID)
    await bot.delete_message(chat_id, bot_message_id)


async def send_message(fsm_storage: FSMStorage, bot: Bot, data: MessageSetting, is_send_new=True):
    is_send_new = True if data.media is not None or data.cache_media is not None else is_send_new
    if data.media is not None:
        await send_media_message(fsm_storage, bot, MessageSetting(media=data.media))

    await send_text_message(fsm_storage, bot, data, is_send_new)



async def send_text_message(fsm_storage: FSMStorage, bot: Bot, data: MessageSetting, is_send_new=True):
    bot_msg_id, chat_id = await fsm_storage.get_data(UserSessionKeys.BOTS_MESSAGE_ID, UserSessionKeys.CHAT_ID)

    if is_send_new:
        bot_msg = await bot.send_message(chat_id=chat_id, text=data.text,
                               reply_markup=data.keyboard, parse_mode=data.parse_mode)
        await fsm_storage.update_value(UserSessionKeys.BOTS_MESSAGE_ID, bot_msg.message_id)
    else:
        await bot.edit_message_text(text=data.text, chat_id=chat_id,
                                    message_id=bot_msg_id, parse_mode=data.parse_mode,
                                    reply_markup=data.keyboard)
