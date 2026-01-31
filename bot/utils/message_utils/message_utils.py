import math
import markdown2

from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest


from .config_obj import MessageSetting
from .media_messages_utils import send_media_message, delete_media_message, reset_media_message

from bot.constants.redis_keys import UserSessionKeys
from bot.storage.redis import FSMStorage


async def delete_bot_message(fsm_storage: FSMStorage, bot: Bot) -> None:
    bot_message_id, chat_id = await fsm_storage.get_data(UserSessionKeys.BOTS_MESSAGE_ID, UserSessionKeys.CHAT_ID)
    try:
        await bot.delete_message(chat_id, bot_message_id)
    except TelegramBadRequest as e:
        pass


async def send_message(fsm_storage: FSMStorage, bot: Bot, data: MessageSetting, is_send_new=True):
    if not is_send_new: await delete_media_message(fsm_storage, bot)
    if data.media is not None and not is_send_new: await delete_bot_message(fsm_storage, bot)

    is_send_new = True if data.media is not None else is_send_new
    if is_send_new and data.media is None:
        await reset_media_message(fsm_storage)

    if data.media is not None:
        await send_media_message(fsm_storage, bot, MessageSetting(media=data.media))

    await send_text_message(fsm_storage, bot, data, is_send_new)



async def send_text_message(fsm_storage: FSMStorage, bot: Bot, data: MessageSetting, is_send_new=True):
    bot_msg_id, chat_id = await fsm_storage.get_data(UserSessionKeys.BOTS_MESSAGE_ID, UserSessionKeys.CHAT_ID)

    if not is_send_new:
        try:
            if isinstance(data.keyboard, ReplyKeyboardMarkup):
                await delete_bot_message(fsm_storage, bot)
                await send_text_message(fsm_storage, bot, data)
            else:
                await bot.edit_message_text(text=data.text, chat_id=chat_id,
                                            message_id=bot_msg_id, parse_mode=data.parse_mode,
                                            reply_markup=data.keyboard)
        except TelegramBadRequest as e:
            print(e)
            if str(e) == "Telegram server says - Bad Request: message can't be edited":
                await delete_bot_message(fsm_storage, bot)
            elif str(e).startswith('Telegram server says - Bad Request: message is not modified:'):
                await delete_bot_message(fsm_storage, bot)
            await send_text_message(fsm_storage, bot, data)
    else:
        bot_msg = await bot.send_message(chat_id=chat_id, text=data.text,
                               reply_markup=data.keyboard, parse_mode=data.parse_mode)
        await fsm_storage.update_value(UserSessionKeys.BOTS_MESSAGE_ID, bot_msg.message_id)
