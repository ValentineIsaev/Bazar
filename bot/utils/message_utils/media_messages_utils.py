import asyncio
from asyncio import Lock

from aiogram import Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from .config_obj import MessageSetting, MediaSetting

# from bot.utils.cache_utils.operators import CacheMediaObj
from bot.types.storage import TelegramMediaSaveData, TelegramMediaLocalConsolidator, FSMStorage, Storage, LocalObjPath

from bot.constants.redis_keys import UserSessionKeys, StorageKeys
from bot.constants.utils_const import TypesMedia


async def reset_media_message(storage: Storage):
    await storage.update_value(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID, None)


async def delete_media_message(storage: Storage, bot: Bot):
    bots_media_message_id, chat_id = await storage.get_data(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID,
                                                              UserSessionKeys.CHAT_ID)
    if bots_media_message_id is not None:
        try:
            if isinstance(bots_media_message_id, int):
                await bot.delete_message(chat_id, bots_media_message_id)
            elif isinstance(bots_media_message_id, list) or isinstance(bots_media_message_id, tuple):
                for msg_id in bots_media_message_id:
                    await bot.delete_message(chat_id, msg_id)
        except TelegramBadRequest as e:
            pass

        await reset_media_message(storage)


async def send_media_message(storage: Storage, bot: Bot, data: MessageSetting) -> None:
    chat_id = await storage.get_value(UserSessionKeys.CHAT_ID)
    if data.media is None:
        raise ValueError('Media data is clear!')

    def input_file(media_setting: MediaSetting) -> str | FSInputFile:
        if media_setting.file_id is not None:
            _file = media_setting.file_id
        elif media_setting.path is not None:
            if not media_setting.path.path.exists():
                raise ValueError(f'File \'{media_setting.path}\' is not exits')
            _file = FSInputFile(media_setting.path.path)
        else:
            raise ValueError('Media setting is clear!')

        return _file

    media_message_id = None
    if isinstance(data.media, tuple):
        media_group = []
        for media in data.media:
            file = input_file(media)
            if len(media_group) == 0 and data.text is not None:
                caption = data.text
            else:
                caption = media.caption

            if media.type_media == TypesMedia.TYPE_PHOTO:
                media_group.append(InputMediaPhoto(media=file, caption=caption))
            elif media.type_media == TypesMedia.TYPE_VIDEO:
                media_group.append(InputMediaVideo(media=file, caption=caption))

        media_message = await bot.send_media_group(chat_id, media=media_group)
        media_message_id = tuple(msg.message_id for msg in media_message)

    elif isinstance(data.media, MediaSetting):
        file = input_file(data.media)

        if data.media.type_media == TypesMedia.TYPE_PHOTO:
            media_message = await bot.send_photo(chat_id, file, caption=data.text,
                                                 parse_mode=data.parse_mode,
                                                 reply_markup=data.keyboard)
        elif data.media.type_media == TypesMedia.TYPE_VIDEO:
            media_message = await bot.send_video(chat_id, file, caption=data.text,
                                                 parse_mode=data.parse_mode,
                                                 reply_markup=data.keyboard)
        media_message_id = media_message.message_id

    if media_message_id is not None:
        await storage.update_value(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID, media_message_id)
