from typing import Callable
from asyncio import Lock

from aiogram import Bot
from aiogram.types import Message, PhotoSize, Video
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from bot.constants.redis_keys import StorageKeys

from bot.types.storage import FSMStorage, TelegramMediaSaveData, TelegramMediaLocalConsolidator
from bot.constants.utils_const import TypesMedia
from bot.types.utils import MessageSetting

from bot.components.errors_renderer import ErrorRenderer


from bot.utils.message_utils import send_message, get_reply_keyboard


SKIP_TEXT = 'Пропустить.'
STOP_TEXT = 'Это все.'

REPLY_TEXT = 'Это все?'

START_KEYBOARD = get_reply_keyboard(SKIP_TEXT)
PROCESSING_KEYBOARD = get_reply_keyboard(SKIP_TEXT, STOP_TEXT)


class InputMediaMiddleWare(BaseMiddleware):
    def __init__(self, media_consolidator: TelegramMediaLocalConsolidator):
        self._global_lock = Lock()
        self._locks = {}

        self._media_consolidator = media_consolidator

    async def start_input(self, fsm_storage: FSMStorage,  start_data: MessageSetting,
                          max_len: int) -> MessageSetting:
        await fsm_storage.update_data(**{StorageKeys.InputMediaAlbum.IS_PROCESSING: True,
                                         StorageKeys.InputMediaAlbum.MAX_LEN: max_len})
        start_data.keyboard = START_KEYBOARD
        return start_data

    def _get_saved_media_data(self, msg: Message) -> TelegramMediaSaveData | None:
        if msg.photo is not None:
            type_media = TypesMedia.TYPE_PHOTO
            file_id = msg.photo[-1].file_id
        elif msg.video is not None:
            type_media = TypesMedia.TYPE_VIDEO
            file_id = msg.video.file_id
        else:
            return None

        return TelegramMediaSaveData(file_id, type_media)

    async def processing_media(self, msg: Message, lock: Lock, storage: FSMStorage) -> bool:
        result = False
        async with lock:
            max_len, prev_bot_msg_id, media = await storage.get_data(
                                                               StorageKeys.InputMediaAlbum.MAX_LEN,
                                                                     StorageKeys.InputMediaAlbum.PREV_BOT_MSG_ID,
                                                                     StorageKeys.InputMediaAlbum.MEDIA,
                                                                    )

            is_over = True if media is not None and len(media) == max_len-1 else False
            if msg.text != STOP_TEXT and msg.text != SKIP_TEXT:
                if media is None: media = []
                media.append(self._get_saved_media_data(msg))

                if prev_bot_msg_id is not None:await msg.bot.delete_message(msg.chat.id, prev_bot_msg_id)
                if not is_over:
                    sent_msg = await msg.answer(text=REPLY_TEXT, reply_markup=PROCESSING_KEYBOARD)
                    prev_bot_msg_id = sent_msg.message_id
            else:
                if prev_bot_msg_id is not None:await msg.bot.delete_message(msg.chat.id, prev_bot_msg_id)
                if media is not None and msg.text != SKIP_TEXT: media = await self._media_consolidator.save_temp_obj(*media)
                result = True

        await storage.update_data(**{StorageKeys.InputMediaAlbum.PREV_BOT_MSG_ID: prev_bot_msg_id,
                                     StorageKeys.InputMediaAlbum.MEDIA: media})
        return result

    async def _reset(self, fsm_storage: FSMStorage):
        await fsm_storage.update_data(**{StorageKeys.InputMediaAlbum.MAX_LEN: None,
                                         StorageKeys.InputMediaAlbum.IS_PROCESSING: False,
                                         StorageKeys.InputMediaAlbum.MEDIA: None,
                                         StorageKeys.InputMediaAlbum.PREV_BOT_MSG_ID: None})

    async def __call__(self, handler, msg: Message, data):
        state = data['state']
        storage = FSMStorage(state)
        is_processing = await storage.get_value(StorageKeys.InputMediaAlbum.IS_PROCESSING)

        if is_processing and isinstance(msg, Message):
            user_id = msg.from_user.id

            async with self._global_lock:
                lock = self._locks.get(user_id)
                if lock is None: lock = Lock(); self._locks[user_id] = lock

            if await self.processing_media(msg, lock, storage):
                data['media'] = await storage.get_value(StorageKeys.InputMediaAlbum.MEDIA)
                await self._reset(storage)
            else:
                return

        await handler(msg, data)
