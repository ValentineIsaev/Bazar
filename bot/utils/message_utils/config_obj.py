from dataclasses import dataclass
from pathlib import Path
import re
from enum import Enum

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from bot.types.storage import LocalObjPath

from bot.constants.utils_const import TypesMedia


@dataclass
class CallbackSetting:
    _CALLBACK_STRUCTURE = r'^[^:]+/[^:]+/[^:]*$'

    scope: str
    subscope: str | None = None
    action: str | None = None

    def __str__(self):
        return self.callback

    @property
    def callback(self):
        return f'{self.scope}/{self.subscope}/{self.action if self.action is not None else ' '}'

    @staticmethod
    def decode_callback(callback: str) -> tuple[str, str, str]:
        if re.search(CallbackSetting._CALLBACK_STRUCTURE, callback):
            return callback.split('/')
        raise ValueError(f'This is not a callback: {callback}')

    @staticmethod
    def encode_callback(scope: str, subscope: str, action: str=' ') -> str:
        return f'{scope}/{subscope}/{action}'

    @staticmethod
    def from_str(cb: str) -> 'CallbackSetting':
        return CallbackSetting(*CallbackSetting.decode_callback(cb))


@dataclass()
class InlineButtonSetting:
    text: str = None
    callback: CallbackSetting = None
    url: str = None


@dataclass
class InputMedia:
    message_id: int
    chat_id: int

    file_id: str
    type_media: TypesMedia


@dataclass
class MediaSetting:
    type_media: TypesMedia
    file_id: str = None
    path: LocalObjPath = None
    caption: str = None


class ParseModes(Enum):
    MARKDOWN_V2 = 'MarkdownV2'


@dataclass
class MessageSetting:
    def __init__(self, text: str=None, keyboard: InlineKeyboardMarkup|ReplyKeyboardMarkup=None, parse_mode:ParseModes=None,
                 media: MediaSetting | tuple[MediaSetting, ...]=None):
        self._text = self._set_text(text, parse_mode=parse_mode)
        self.keyboard = keyboard
        self._parse_mode = parse_mode
        self.media = media

    @property
    def parse_mode(self):
        return self._parse_mode.value if self._parse_mode is not None else None

    @staticmethod
    def escape_markdown(text: str) -> str:
        escape_chars = r'_*[]()~`>#+-=|{}.!'
        return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = self._set_text(value, self._parse_mode)

    def _markdown_escape(self, text: str) -> str:
        result = ''
        for char in text:
            if char in ('.', '!', '-', '+') and result[-1] != '\\':
                result += '\\'
            result += char
        return result

    def _set_text(self, text: str | None, parse_mode: ParseModes) -> str | None:
        if text is not None:
            if parse_mode == ParseModes.MARKDOWN_V2:
                return self._markdown_escape(text)
            return text
        return None


class TextTemplate:
    def __init__(self, text: str):
        self.__text = text

    def insert(self, new_value: tuple | list) -> str:
        parts = self.__text.split('?')
        return ''.join(
            (part if i > len(new_value)-1 else part + str(new_value[i])) for i, part in enumerate(parts))