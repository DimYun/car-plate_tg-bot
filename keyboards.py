from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)


def kb_location() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Sent geolocation", request_location=True)
    kb.button(text="Change photo")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def kb_location_result() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Yes")
    kb.button(text="Change geolocation", request_location=True)
    return kb.as_markup(resize_keyboard=True)


def kb_payment() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Pay", callback_data="pay")
    return kb.as_markup()
