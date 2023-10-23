from typing import Union

from aiogram import Router, types, filters, F

from config import DB_PATH, MAX_SECRETS_PER_USER
from data_workers.sqlite_manager import SQLiteManager
from keyboards.client_keyboards import *
from main import bot
from utils.identifyer_generator import generate_unique_key


router = Router()
manager = SQLiteManager(DB_PATH)


class UserStateFilter(filters.BaseFilter):
    def __init__(self, user_status: Union[int, list]):
        self.user_status = user_status

    async def __call__(self, message: types.Message) -> bool:
        if isinstance(self.user_status, int):
            return manager.get_user_status(message.chat.id) == self.user_status
        else:
            return manager.get_user_status(message.chat.id) in self.user_status


@router.message(filters.Command("start"), UserStateFilter(0))
async def command_start(message: types.Message):
    if not manager.is_user_registered(message.chat.id):
        manager.register_new_user(message.chat.id)

    await message.answer("<b>Привет 👋, Аноним!</b>\n\n"
                         "Добро пожаловать в полностью анонимный чат-бот! 🤖\n\n"
                         "Здесь ты можешь общаться со случайными собеседниками или создать свой уникальный "
                         "идентификационный код и передать его кому посчитаешь нужным. 🔑\n"
                         "Главная фишка такого чата - это полная анонимность! Твой собеседник никогда не узнает твою "
                         "личность, если ты сам этого не захочешь. 😎\n\n"
                         "<b><i>Давай начнем общение! 💬 Используй кнопки ниже.</i></b>", reply_markup=main_kb())


@router.message(F.text == "🔎 Начать поиск", UserStateFilter(0))
async def start_find_button_click(message: types.Message):
    await message.answer("<b>Начинаю поиск случайного собеседника... 🕵️ ‍Ожидайте...</b>", reply_markup=in_find_kb())
    manager.update_user_status(message.chat.id, 1)

    if companion := manager.find_companion(message.chat.id):
        manager.update_user_status(message.chat.id, 2)
        manager.update_user_status(companion[0], 2)
        manager.register_new_chat(message.chat.id, companion[0])
        await message.answer("<b>Ура! 🎉 Собеседник найден! Хорошего общения.</b>", reply_markup=in_chat_kb())
        await bot.send_message(companion[0], "<b>Ура! 🎉 Собеседник найден! Хорошего общения.</b>", reply_markup=in_chat_kb())


@router.message(F.text == "🛑 Прекратить поиск", UserStateFilter(1))
async def start_find_button_click(message: types.Message):
    manager.update_user_status(message.chat.id, 0)
    await message.answer("<b>Прекращаю поиск собеседника. 🚫</b>", reply_markup=main_kb())


@router.message(F.text == "🛑 Остановить диалог", UserStateFilter(2))
async def stop_dialog_button_click(message: types.Message):
    chat_participants = manager.find_chat_by_id(message.chat.id)
    companion_id = sum(chat_participants) - message.chat.id

    manager.update_user_status(message.chat.id, 0)
    manager.update_user_status(companion_id, 0)

    manager.delete_chat(message.chat.id)
    await message.answer("<b>Ваш диалог был остановлен по вашей инициативе. 🚫</b>", reply_markup=main_kb())
    await bot.send_message(companion_id, "<b>Ваш диалог был остановлен по инициативе собеседника. 🚫</b>",
                           reply_markup=main_kb())


@router.message(F.text == "🔐 Сгенерировать код подключения", UserStateFilter([0, 2]))
async def generate_secret_handler(message: types.Message):
    if manager.count_user_secrets(message.chat.id) >= MAX_SECRETS_PER_USER:
        await message.answer("<b>Достигнуто максимальное количество уникальных кодов подключения. "
                             "🚫 Используйте старые.</b>")
        return

    new_secret = generate_unique_key(message.chat.id)
    manager.add_user_secret(message.chat.id, new_secret)
    await message.answer(f"<b>Ваш новый уникальный код подключения 🔐: <tg-spoiler>{new_secret}</tg-spoiler></b>")


@router.message(F.text == "🔓 Подключиться по ключу", UserStateFilter(0))
async def wait_connection_secret(message: types.Message):

    await message.answer("<b>Хорошо, отправь мне уникальный ключ подключения пользователя... 🔑</b>",
                         reply_markup=clear_kb())
    manager.update_user_status(message.chat.id, 3)


@router.message(F.text, UserStateFilter(3))
async def check_connection_secret(message: types.Message):
    if len(message.text) != 64:
        await message.answer("<b>Неверный формат ключа. ❌ Проверьте правильность ввода "
                             "или уточните его у владельца</b>", reply_markup=main_kb())
        manager.update_user_status(message.chat.id, 0)
        return

    desired_companion = manager.find_user_by_secret(message.text)

    if not desired_companion:
        await message.answer("<b>По данному ключу пользователь не найден, или ключ уже не актуален. ❌</b>",
                             reply_markup=main_kb())
        manager.update_user_status(message.chat.id, 0)
        return

    if desired_companion[0] == message.chat.id:
        await message.answer("<b>Вы не можете подключиться к себе же. ❌ Передайте этот ключ другому пользователю, "
                             "чтобы он мог связаться с вами в любой момент.</b>",
                             reply_markup=main_kb())
        manager.update_user_status(message.chat.id, 0)
        return

    if manager.find_chat_by_id(desired_companion[0]):
        await message.answer("<b>Пользователь находится в диалоге, попробуйте позже. ⏳</b>",
                             reply_markup=main_kb())
        manager.update_user_status(message.chat.id, 0)
        return

    manager.delete_user_secret(message.text)
    manager.update_user_status(message.chat.id, 2)
    manager.update_user_status(desired_companion[0], 2)
    manager.register_new_chat(message.chat.id, desired_companion[0])
    await message.answer("<b>Подключаю вас к пользователю! 🔄 Хорошего общения.</b>", reply_markup=in_chat_kb())
    await bot.send_message(desired_companion[0], "<b>С вами связывается пользователь, используя следующий ключ:\n"
                                                 f"<tg-spoiler>{message.text}</tg-spoiler>\n"
                                                 f"Более этот ключ не актуален. ❗</b>", reply_markup=in_chat_kb())


@router.message(UserStateFilter(2))
async def conversation(message: types.Message):
    chat_participants = manager.find_chat_by_id(message.chat.id)
    companion_id = sum(chat_participants) - message.chat.id

    await message.copy_to(companion_id)


@router.message()
async def conversation(message: types.Message):
    await message.delete()
