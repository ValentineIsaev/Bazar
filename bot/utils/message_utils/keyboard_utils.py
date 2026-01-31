from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import inline_keyboard_markup

from .config_obj import InlineButtonSetting

def get_reply_keyboard(*text) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text_button)] for text_button in text],
                               one_time_keyboard=True,
                               resize_keyboard=True)


def get_callback_inline_keyboard(*data: InlineButtonSetting, row=1,
                                 keyboard_markup: inline_keyboard_markup=None) -> inline_keyboard_markup:
    keyboard = InlineKeyboardBuilder() if keyboard_markup is None else InlineKeyboardBuilder.from_markup(keyboard_markup)

    for i in range(0, len(data), row):
        layer = data[i:i+row]
        keyboard.row(
            *[InlineKeyboardButton(text=button.text, callback_data=button.callback.callback) for button in layer])

    return keyboard.as_markup()
