import math

from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import Message

from bot.utils.message_utils.message_setting_classes import MessageSetting
from .media_messages_utils import send_media_message, send_cached_media_message

from bot.configs.constants import ParamFSM
from bot.utils.helper import get_data_state


async def delete_bot_message(state: FSMContext) -> None:
    bot_message: Message
    (bot_message,) = await get_data_state(state, ParamFSM.BotMessagesData.BOT_MESSAGE)

    await bot_message.delete()


async def send_message(state: FSMContext, bot: Bot, data: MessageSetting, is_send_new=True):
    is_send_new = True if data.media is not None or data.cache_media is not None else is_send_new
    if data.media is not None:
        await send_media_message(state, bot, MessageSetting(media=data.media))
    if data.cache_media is not None:
        await send_cached_media_message(state, bot, MessageSetting(cache_media=data.cache_media))

    await send_text_message(state, bot, data, is_send_new)



async def send_text_message(state: FSMContext, bot: Bot, data: MessageSetting, is_send_new=True):
    bot_msg, chat_id = await get_data_state(state, ParamFSM.BotMessagesData.BOT_MESSAGE,
                                            ParamFSM.BotMessagesData.CHAT_ID)

    if is_send_new:
        bot_msg = await bot.send_message(chat_id=chat_id, text=data.text,
                               reply_markup=data.keyboard, parse_mode=data.parse_mode)
        await state.update_data(**{ParamFSM.BotMessagesData.BOT_MESSAGE: bot_msg})
    else:
        await bot.edit_message_text(text=data.text, chat_id=chat_id,
                                    message_id=bot_msg.message_id, parse_mode=data.parse_mode,
                                    reply_markup=data.keyboard)


def create_list_message(values: tuple[...] | list[...], columns: int, partition: str= 5*'\t') -> str:
    result = ''
    lines = math.ceil(len(values) / columns)

    for i in range(lines):
        for j in range(columns):
            index = i + j * lines
            if index < len(values):
                result += f'{str(values[index])}{partition}'
        result += '\n'

    return result
