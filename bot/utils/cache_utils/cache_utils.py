from .operators import CacheMediaOperator

from aiogram.types import Message
from aiogram import Bot


async def caching_media(media_msg: list[Message] | Message, bot: Bot) -> CacheMediaOperator:
    """
    This func create cache obj and caching media data from user message
    :param media_msg: User input media
    :param bot: aiogram bot for caching and download media file
    :return: CacheMediaOperator
    """
    cache_media = CacheMediaOperator()
    if isinstance(media_msg, list):
        media = []
        for msg in media_msg:
            if msg.photo is not None:
                media.append(msg.photo[-1])
            elif msg.video is not None:
                media.append(msg.video)

        await cache_media.caching_data(media, bot)
        for msg in media_msg:
            await msg.delete()

    elif isinstance(media_msg, Message):
        if media_msg.photo is not None:
            await cache_media.caching_data(media_msg.photo[-1], bot)
        elif media_msg.video is not None:
            await cache_media.caching_data(media_msg.video, bot)
        await media_msg.delete()

    return cache_media
