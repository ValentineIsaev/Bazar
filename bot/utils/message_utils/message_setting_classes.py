from dataclasses import dataclass
from pathlib import Path

from aiogram.types import inline_keyboard_markup

from bot.utils.cache_utils.cache_obj import CacheMediaObj


@dataclass
class MediaSetting:
    TYPE_PHOTO = 'photo'
    TYPE_VIDEO = 'video'

    type_media: str

    file_id: str = None
    path: Path = None


@dataclass
class MessageSetting:
    def __init__(self, text: str, keyboard: inline_keyboard_markup=None, parse_mode:str=None,
                 media: MediaSetting | tuple[MediaSetting]=None,
                 cache_media: CacheMediaObj | tuple[CacheMediaObj]=None):
        self.text = text
        self.keyboard = keyboard
        self.parse_mode = parse_mode
        self.media = media
        self.cache_media = cache_media


class TextTemplate:
    def __init__(self, text: str):
        self.__text = text

    def insert(self, new_value: tuple| list) -> str:
        parts = self.__text.split('?')
        return ''.join(
            (part if i > len(new_value)-1 else part + str(new_value[i])) for i, part in enumerate(parts))