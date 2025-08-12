from aiogram import Bot
from aiogram.types import Message, FSInputFile, PhotoSize, Video
from aiogram.fsm.context import FSMContext

from bot.utils.message_utils.message_utils import MessageSetting, send_message, delete_bot_message
from bot.utils.helper import get_data_state
from bot.utils.message_utils.message_setting_classes import MediaSetting

from bot.utils.cache_utils.operators import CacheMediaOperator, CacheMediaObj

from bot.configs.constants import ParamFSM


TYPES_INPUT_USER_MEDIA = ('photo', 'video')
async def input_media_album(state: FSMContext, msg: Message,  stop_text: str,
                            answer_message: MessageSetting) -> None | list[PhotoSize | Video]:
    media_list = await state.get_value(ParamFSM.BotMessagesData.INPUTS_MEDIA)
    if media_list is None:
        media_list = []
        await state.update_data(**{ParamFSM.BotMessagesData.INPUTS_MEDIA: media_list})

    if len(media_list) > 0:
        await delete_bot_message(state, msg.bot)
    if msg.text == stop_text:
        await state.update_data(**{ParamFSM.BotMessagesData.INPUTS_MEDIA: None})
        return media_list
    else:
        media_list.append(msg)

        await send_message(state, msg.bot, answer_message, True)



async def make_cache_media_operator(media_msg: list[Message] | Message, bot: Bot) -> CacheMediaOperator:
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

    def add_media_from_path() -> FSInputFile:
        if not data.media.path.exists():
            raise ValueError(f'File \'{data.media}\' is not exits')
        return FSInputFile(data.media.path)

    def add_media_from_server():
        pass

    if isinstance(data.media, tuple):
        pass
    elif isinstance(data.media, MediaSetting):
        if data.media.file_id is not None:
            pass
        elif data.media.path is not None:
            file = add_media_from_path()

        if data.media.type_media == data.media.TYPE_PHOTO:
            media_message = await bot.send_photo(chat_id, file, caption=data.text,
                                                 parse_mode=data.parse_mode,
                                                 reply_markup=data.keyboard)

    await state.update_data(**{ParamFSM.BotMessagesData.BOT_MEDIA_MESSAGE: media_message})
