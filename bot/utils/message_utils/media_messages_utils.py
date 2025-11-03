import asyncio

from aiogram import Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext

from .config_obj import MessageSetting, MediaSetting, InputMedia

# from bot.utils.cache_utils.operators import CacheMediaObj
from bot.types.storage import TelegramMediaSaveData
from bot.storage.redis import Storage

from bot.constants.redis_keys import UserSessionKeys, FSMKeys
from bot.constants.utils_const import TypesMedia


async def delete_media_message(storage: Storage, bot: Bot):
    bots_media_message_id, chat_id = await storage.get_data(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID,
                                                              UserSessionKeys.CHAT_ID)
    if bots_media_message_id is not None:
        if isinstance(bots_media_message_id, int):
            await bot.delete_message(chat_id, bots_media_message_id)
        elif isinstance(bots_media_message_id, list):
            for msg_id in bots_media_message_id:
                await bot.delete_message(chat_id, msg_id)

        await storage.update_value(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID, None)


def parse_media_data(msg: Message) -> TelegramMediaSaveData:
    if msg.photo is not None:
        type_media = TypesMedia.TYPE_PHOTO
        file_id = msg.photo[-1].file_id
    elif msg.video is not None:
        type_media = TypesMedia.TYPE_VIDEO
        file_id = msg.video.file_id
    else:
        raise ValueError('Message have not media!')

    print(file_id)
    return TelegramMediaSaveData(file_id, type_media)


def get_saved_media_data(msg: Message) -> TelegramMediaSaveData:
    if msg.photo is not None:
        type_media = TypesMedia.TYPE_PHOTO
        file_id = msg.photo[-1].file_id
    elif msg.video is not None:
        type_media = TypesMedia.TYPE_VIDEO
        file_id = msg.video.file_id
    else:
        raise ValueError('Message have not media!')

    return TelegramMediaSaveData(file_id, type_media)


lock = asyncio.Lock()
async def input_media_album(bot: Bot, state: FSMContext, msg: Message,  answer_message: MessageSetting,
                            stop_text: str, max_len: int = 3) -> list | list[TelegramMediaSaveData]:
    async with lock:
        result = []
        media_list_id: list[dict[str, TelegramMediaSaveData | int]] | None = await state.get_value(FSMKeys.InputMediaAlbum.INPUTS_MEDIA_MESSAGES_ID)
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


                result = [data.get('data') for data in media_list_id]
                for data in media_list_id:
                    await bot.delete_message(msg.chat.id, data.get('msg_id'))

                bots_messages_id = None
                media_list_id = None

                if is_full and msg.text is None:
                    result.append(parse_media_data(msg))
                    await msg.delete()

                print(tuple(map(lambda x: x.file_id, result)))
            else:
                await msg.delete()
        else:
            media_list_id.append({'data': parse_media_data(msg),
                                  'msg_id': msg.message_id})

            sent_message = await msg.answer(answer_message.text,
                                            parse_mode=answer_message.parse_mode,
                                            reply_markup=answer_message.keyboard)
            bots_messages_id.append(sent_message.message_id)

        await state.update_data(**{FSMKeys.InputMediaAlbum.INPUTS_MEDIA_MESSAGES_ID:
                                       media_list_id,
                                   FSMKeys.InputMediaAlbum.SENT_BOTS_MESSAGES_ID:
                                   bots_messages_id})

        return result


async def send_media_message(storage: Storage, bot: Bot, data: MessageSetting) -> None:
    chat_id = await storage.get_value(UserSessionKeys.CHAT_ID)
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
        await storage.update_value(UserSessionKeys.BOTS_MEDIA_MESSAGE_ID, media_message_id)
