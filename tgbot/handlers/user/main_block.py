from typing import Literal

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from create_bot import bot
from tgbot.handlers.user.inline import InlineKeyboard
from tgbot.handlers.user.reply import UserReplyKeyboard
from tgbot.models.sql_connector import UsersDAO, AwardsDAO
from tgbot.services.google_sheets import GoogleSheets

router = Router()
inline = InlineKeyboard()
reply = UserReplyKeyboard()

google = GoogleSheets()


@router.message(F.text == "В начало")
@router.message(Command("start"))
async def main_block(message: Message, state: FSMContext):
    text = "ГЛАВНОЕ МЕНЮ"
    kb = reply.main_menu_kb()
    await message.answer(text, reply_markup=kb)


async def user_balance_render(user_id: str | int, phone: str):
    balance_data = google.get_user_data(phone=phone)
    if balance_data:
        status = balance_data["status"] if balance_data["status"] != 0 else "---"
        text = [
            f"<u>{balance_data['name']}</u>",
            f"<b>Баланс:</b> {balance_data['balance']}",
            f"<b>Статус в программе лояльности:</b> {status}"
        ]
    else:
        text = ["🤷 Ничего не найдено"]
    kb = reply.main_menu_kb()
    await bot.send_message(chat_id=user_id, text="\n".join(text), reply_markup=kb)


@router.message(F.text == "💰 Узнать баланс")
async def main_block(message: Message):
    await message.delete()
    user = await UsersDAO.get_one_or_none(user_id=str(message.from_user.id))
    if user:
        await user_balance_render(user_id=message.from_user.id, phone=user["phone"])
    else:
        text = "Чтобы мы могли убедиться, что Вы это Вы необходимо подтвердить свой номер телефона кнопкой ниже 👇"
        kb = reply.request_phone_kb()
        await message.answer(text, reply_markup=kb)


@router.message(F.text == "📝 Список вознаграждений")
async def main_block(message: Message):
    await message.delete()
    text = "Выберите тип вознаграждений"
    kb = reply.awards_menu_kb()
    await message.answer(text, reply_markup=kb)


async def awards_render(user_id: str | int, award_type: Literal["with_write_downs", "without_write_downs"]):
    awards = await AwardsDAO.get_many(type_award=award_type)
    kb = reply.main_menu_kb()
    if len(awards) > 0:
        for award in awards:
            text = [
                f"<u>{award['title']}</u>\n",
                award["description"],
            ]
            await bot.send_photo(chat_id=user_id, photo=award["photo_id"], caption="\n".join(text), reply_markup=kb)
    else:
        text = "🤷 Ничего не найдено"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=kb)


@router.message(F.text == "Вознаграждения без списания баллов")
async def main_block(message: Message):
    await message.delete()
    await awards_render(user_id=message.from_user.id, award_type="without_write_downs")


@router.message(F.text == "Вознаграждения со списанием баллов")
async def main_block(message: Message):
    await message.delete()
    await awards_render(user_id=message.from_user.id, award_type="with_write_downs")


@router.message(F.contact)
async def main_block(message: Message):
    username = f"@{message.from_user.username}" if message.from_user.username else "---"
    await UsersDAO.create(user_id=str(message.from_user.id), username=username, phone=message.contact.phone_number)
    await user_balance_render(user_id=message.from_user.id, phone=message.contact.phone_number)


@router.message(F.text == "💡 Обменять баллы")
async def main_block(message: Message):
    await message.delete()
    text = "Для обмена баллов свяжитесь с администратором\n📞 +7 905 876-67-67\n🌐 https://vk.com/yodapc"
    await message.answer(text, disable_web_page_preview=True)
