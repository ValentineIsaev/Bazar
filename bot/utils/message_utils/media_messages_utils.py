from aiogram import Bot
from aiogram.types import Message, FSInputFile, PhotoSize, Video, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext

from ..message_utils.message_setting_classes import TypesMedia

from bot.utils.message_utils.message_utils import MessageSetting, send_message, delete_bot_message
from bot.utils.helper import get_data_state
from bot.utils.message_utils.message_setting_classes import MediaSetting

from bot.utils.cache_utils.operators import CacheMediaOperator, CacheMediaObj

from bot.configs.constants import ParamFSM


async def input_media_album(state: FSMContext, msg: Message,  stop_text: str,
                            answer_message: MessageSetting) -> None | list[Message]:
    media_list = await state.get_value(ParamFSM.BotMessagesData.INPUTS_MEDIA)
    if media_list is None:
        media_list = []
        await state.update_data(**{ParamFSM.BotMessagesData.INPUTS_MEDIA: media_list})

    # if len(media_list) > 0:
    #     await delete_bot_message(state, msg.bot)
    if msg.text == stop_text:
        await state.update_data(**{ParamFSM.BotMessagesData.INPUTS_MEDIA: None})
        return media_list
    else:
        media_list.append(msg)

        await send_message(state, msg.bot, answer_message, True)

    return None


async def send_cached_media_message(state: FSMContext, bot: Bot, data: MessageSetting) -> None:
    if isinstance(data.cache_media, tuple):
        media_path = tuple(MediaSetting(path=media.path, type_media=media.type_media)
                           for media in data.cache_media)
    elif isinstance(data.cache_media, CacheMediaObj):
        media_path = MediaSetting(path=data.cache_media.path,
                                  type_media=data.cache_media.type_media)
    else:
        raise ValueError(f'Wrong type cache media: {type(data.cache_media)}')
    data.media = media_path

    await send_media_message(state, bot, data)


async def send_media_message(state: FSMContext, bot: Bot, data: MessageSetting) -> None:
    (chat_id,) = await get_data_state(state, ParamFSM.BotMessagesData.CHAT_ID)
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

    media_message = None
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

    if media_message is not None:
        await state.update_data(**{ParamFSM.BotMessagesData.BOT_MEDIA_MESSAGE: media_message})
