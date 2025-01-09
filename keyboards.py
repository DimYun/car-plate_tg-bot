from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, ReplyKeyboardBuilder, ReplyKeyboardMarkup

def kb_location() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отправить геолокацию", request_location=True),
    kb.button(text="Изменить фото")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def kb_location_result() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да"),
    kb.button(text="Изменить геолокацию", request_location=True)
    return kb.as_markup(resize_keyboard=True)

def kb_payment() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Оплатить", callback_data="pay")
    return kb.as_markup()

