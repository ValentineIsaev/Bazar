from dataclasses import dataclass
from pathlib import Path
import re

from aiogram.types import inline_keyboard_markup

from bot.utils.cache_utils.cache_obj import CacheMediaObj
from .const import TypesMedia


@dataclass()
class InlineButtonSetting:
    text: str = None
    callback: str = None
    url: str = None


@dataclass
class CallbackSetting:
    _CALLBACK_STRUCTURE = r'^[^:]+/[^:]+/[^:]+$'

    scope: str
    subscope: str | None = None
    action: str | None = None

    @property
    def callback(self):
        return f'{self.scope}:{self.subscope}:{self.action}'

    @staticmethod
    def decode_callback(callback: str) -> tuple[str, str, str]:
        if re.search(CallbackSetting._CALLBACK_STRUCTURE, callback):
            return callback.split('/')
        raise ValueError('This is not a callback')

    @staticmethod
    def encode_callback(scope: str, subscope: str, action: str) -> str:
        return f'{scope}/{subscope}/{action}'


@dataclass
class InputMedia:
    message_id: int
    chat_id: int

    file_id: str
    type_media: TypesMedia


@dataclass
class MediaSetting:
    type_media: str

    file_id: str = None
    path: Path = None

    caption: str = None


@dataclass
class MessageSetting:
    def __init__(self, text: str=None, keyboard: inline_keyboard_markup=None, parse_mode:str=None,
                 media: MediaSetting | tuple[MediaSetting]=None):
        self.text = text
        self.keyboard = keyboard
        self.parse_mode = parse_mode
        self.media = media
        # self.cache_media = cache_media


class TextTemplate:
    def __init__(self, text: str):
        self.__text = text

    def insert(self, new_value: tuple| list) -> str:
        parts = self.__text.split('?')
        return ''.join(
            (part if i > len(new_value)-1 else part + str(new_value[i])) for i, part in enumerate(parts))