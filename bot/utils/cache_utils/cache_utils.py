from .operators import CacheMediaOperator

from aiogram.types import Message
from aiogram import Bot

from ..message_utils.message_setting_classes import InputMedia


async def caching_media(media_msg: list[InputMedia] | InputMedia, bot: Bot) -> CacheMediaOperator:
    """
    This func create cache obj and caching media data from user message
    :param media_msg: msg id with media
    :param bot: aiogram bot for caching and download media file
    :return: CacheMediaOperator
    """
    cache_media = CacheMediaOperator()
    if isinstance(media_msg, list):
        for msg in media_msg:
            await bot.delete_message(msg.chat_id, msg.message_id)
    elif isinstance(media_msg, InputMedia):
        await bot.delete_message(media_msg.chat_id, media_msg.message_id)

    await cache_media.caching_data(media_msg, bot)
    return cache_media
