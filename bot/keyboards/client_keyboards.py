from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove


def main_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.button(text="🔎 Начать поиск")
    kb_builder.button(text="🔐 Сгенерировать код подключения")
    kb_builder.button(text="🔓 Подключиться по ключу")
    kb_builder.adjust(1)
    return kb_builder.as_markup(resize_keyboard=True)


def in_find_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.button(text="🛑 Прекратить поиск")
    return kb_builder.as_markup(resize_keyboard=True)


def in_chat_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.button(text="🛑 Остановить диалог")
    kb_builder.button(text="🔐 Сгенерировать код подключения")
    kb_builder.adjust(1)
    return kb_builder.as_markup(resize_keyboard=True)


def clear_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
