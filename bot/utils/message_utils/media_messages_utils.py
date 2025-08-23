import asyncio
from dataclasses import dataclass

from aiogram import Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext

from ..message_utils.message_setting_classes import TypesMedia, MessageSetting, MediaSetting, InputMedia

from bot.utils.cache_utils.operators import CacheMediaObj
from bot.managers.session_manager.session import UserSession

from bot.constants.redis_keys import UserSessionKeys, FSMKeys


async def delete_media_message(session: UserSession, bot: Bot):
    bots_media_message_id, chat_id = await session.get_values(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID,
                                                              UserSessionKeys.CHAT_ID)
    if bots_media_message_id is not None:
        if isinstance(bots_media_message_id, int):
            await bot.delete_message(chat_id, bots_media_message_id)
        elif isinstance(bots_media_message_id, list):
            for msg_id in bots_media_message_id:
                await bot.delete_message(chat_id, msg_id)

        await session.set_value(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID, None)


def parse_media_data(msg: Message) -> InputMedia:
    type_media = ''
    file_id = ''
    if msg.photo is not None:
        type_media = TypesMedia.TYPE_PHOTO
        file_id = msg.photo[-1].file_id
    elif msg.video is not None:
        type_media = TypesMedia.TYPE_VIDEO
        file_id = msg.video.file_id

    return InputMedia(msg.message_id, msg.chat.id, file_id, type_media)


lock = asyncio.Lock()
async def input_media_album(bot: Bot, state: FSMContext, msg: Message,  answer_message: MessageSetting,
                            stop_text: str, max_len: int = 3) -> list | list[InputMedia]:
    async with lock:
        result = []
        media_list_id: list[InputMedia] | None = await state.get_value(FSMKeys.InputMediaAlbum.INPUTS_MEDIA_MESSAGES_ID)
        bots_messages_id: list[int] | None = await state.get_value(FSMKeys.InputMediaAlbum.SENT_BOTS_MESSAGES_ID)
        if media_list_id is None:
            media_list_id = []
        if bots_messages_id is None:
            bots_messages_id = []

        if len(bots_messages_id) > 0:
            await bot.delete_message(msg.chat.id, bots_messages_id[0])
            bots_messages_id.pop(0)

        is_full = len(media_list_id) >= max_len - 1

        if msg.text is not None or is_full:
            if msg.text == stop_text or is_full:
                if msg.text == stop_text:
                    await msg.delete()

                for bot_message_id in bots_messages_id:
                    await bot.delete_message(msg.chat.id, bot_message_id)

                result = media_list_id

                bots_messages_id = None
                media_list_id = None

                if is_full and msg.text is None:
                    result.append(parse_media_data(msg))
            else:
                await msg.delete()
        else:
            media_list_id.append(parse_media_data(msg))

            sent_message = await msg.answer(answer_message.text,
                                            parse_mode=answer_message.parse_mode,
                                            reply_markup=answer_message.keyboard)
            bots_messages_id.append(sent_message.message_id)

        await state.update_data(**{FSMKeys.InputMediaAlbum.INPUTS_MEDIA_MESSAGES_ID:
                                       media_list_id,
                                   FSMKeys.InputMediaAlbum.SENT_BOTS_MESSAGES_ID:
                                   bots_messages_id})

        return result


async def send_cached_media_message(session: UserSession, bot: Bot, data: MessageSetting) -> None:
    if isinstance(data.cache_media, tuple):
        media_path = tuple(MediaSetting(path=media.path, type_media=media.type_media)
                           for media in data.cache_media)
    elif isinstance(data.cache_media, CacheMediaObj):
        media_path = MediaSetting(path=data.cache_media.path,
                                  type_media=data.cache_media.type_media)
    else:
        raise ValueError(f'Wrong type cache media: {type(data.cache_media)}')
    data.media = media_path

    await send_media_message(session, bot, data)


async def send_media_message(session: UserSession, bot: Bot, data: MessageSetting) -> None:
    chat_id = await session.get_value(UserSessionKeys.CHAT_ID)
    if data.media is None:
        raise ValueError('Media data is clear!')

    def input_file(media_setting: MediaSetting) -> str | FSInputFile:
        if media_setting.file_id is not None:
            _file = media_setting.file_id
        elif media_setting.path is not None:
            if not media_setting.path.exists():
                raise ValueError(f'File \'{media_setting.path}\' is not exits')
            _file = FSInputFile(media_setting.path)
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
        await session.set_value(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID, media_message_id)
