from aiogram import Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo, PhotoSize, Video
from aiogram.fsm.context import FSMContext

from bot.utils.cache_utils.operators import CacheMediaOperator, CacheMediaObj
from .message_utils import MessageSetting, send_message, delete_bot_message
from .helper import get_data_state

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


async def send_media_message(state: FSMContext, bot: Bot, data: MessageSetting) -> None:
    (chat_id,) = await get_data_state(state, ParamFSM.BotMessagesData.CHAT_ID)
    media: CacheMediaObj = data.media_cache_operator.data
    if isinstance(media, CacheMediaObj):
        if media.type_media == CacheMediaObj.TYPE_PHOTO:
            photo = FSInputFile(media.path)
            media_message = await bot.send_photo(chat_id, photo, caption=data.text, reply_markup=data.keyboard)

        elif media.type_media == CacheMediaObj.TYPE_VIDEO:
            video = FSInputFile(media.path)
            media_message = await bot.send_video(chat_id, video, caption=data.text, reply_markup=data.keyboard)

        else:
            raise TypeError(f'Wrong type media: {media.type_media}')

    elif isinstance(media, tuple):
        media_group = []
        media_obj: CacheMediaObj
        for index, media_obj in enumerate(media):
            caption, parse_mode = data.text, data.parse_mode if index == 0 else None
            input_data = {'media':media_obj.path, 'caption':caption, 'parse_mode':parse_mode}
            if media_obj.type_media == CacheMediaObj.TYPE_PHOTO:
                media_group.append(InputMediaPhoto(**input_data))
            elif media_obj.type_media == CacheMediaObj.TYPE_VIDEO:
                media_group.append(InputMediaVideo(**input_data))

        media_message = await bot.send_media_group(chat_id, media=media_group)
    else:
        media_message = None

    await state.update_data(**{ParamFSM.BotMessagesData.BOT_MEDIA_MESSAGE: media_message})
