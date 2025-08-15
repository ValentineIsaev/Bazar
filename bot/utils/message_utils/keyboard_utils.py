from dataclasses import dataclass
import re

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import inline_keyboard_markup

@dataclass()
class InlineButtonSetting:
    text: str = None
    callback: str = None
    url: str = None


def _builder_inline_keyboard(*data: InlineButtonSetting,
                             builder: InlineKeyboardBuilder, row=1) -> InlineKeyboardBuilder:
    for i in range(0, len(data), row):
        layer = data[i:i+row]
        builder.row(
            *[InlineKeyboardButton(text=button.text, callback_data=button.callback) for button in layer])

    return builder


def create_reply_keyboard(*text) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text_button)] for text_button in text],
                               one_time_keyboard=True,
                               resize_keyboard=True)


def create_callback_inline_keyboard(*data: InlineButtonSetting, row=1) -> inline_keyboard_markup:
    keyboard = InlineKeyboardBuilder()
    keyboard = _builder_inline_keyboard(*data, builder=keyboard, row=row)
    return keyboard.as_markup()


def add_callback_inline_keyboard(markup: inline_keyboard_markup,
                                 *data: InlineButtonSetting, row=1) -> inline_keyboard_markup:
    builder = InlineKeyboardBuilder.from_markup(markup)
    builder = _builder_inline_keyboard(*data, builder=builder, row=row)

    return builder.as_markup()


def generate_number_buttons(start: int, end: int, scope: str, subscope: str, action: str):
    return tuple(InlineButtonSetting(text=str(number+1),
                                     callback=create_callback(scope,
                                                         subscope,
                                                         f'{action}-{number}')) for number in range(start, end))


CALLBACK_STRUCTURE = r'^[^:]+:[^:]+:[^:]+$'


def create_callback(scope: str, subscope: str, action: str) -> str:
    return f'{scope}:{subscope}:{action}'

def parse_callback(callback: str) -> tuple[str, str, str]:
    if re.search(CALLBACK_STRUCTURE, callback):
        return callback.split(':')
    raise ValueError('This is not a callback')