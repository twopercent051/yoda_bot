from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router

from create_bot import bot, config
from .filters import AdminFilter
from .inline import InlineKeyboard
from tgbot.misc.states import AdminFSM
from ...models.sql_connector import AwardsDAO

router = Router()
router.message.filter(AdminFilter())

admin_group = config.tg_bot.admin_group

inline = InlineKeyboard()


@router.message(Command("start"))
async def main_block(message: Message, state: FSMContext):
    text = "Главное меню"
    kb = inline.main_menu_kb()
    await state.set_state(AdminFSM.home)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "home")
async def main_block(callback: CallbackQuery, state: FSMContext):
    text = "Главное меню"
    kb = inline.main_menu_kb()
    await state.set_state(AdminFSM.home)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == "edit_awards")
async def main_block(callback: CallbackQuery):
    awards = await AwardsDAO.get_all()
    text = "Выберите запись для просмотра или создайте новую"
    kb = inline.awards_list_kb(awards=awards)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "award")
async def main_block(callback: CallbackQuery):
    award_id = int(callback.data.split(":")[1])
    award_profile = await AwardsDAO.get_one_or_none(id=award_id)
    if award_profile:
        write_downs_dict = dict(with_write_downs="Со списанием", without_write_downs="Без списания")
        text = [
            f"<u>{award_profile['title']}</u>\n",
            award_profile["description"],
            f"\n<b>Цена:</b> {award_profile['price']}",
            write_downs_dict[award_profile["type_award"]]
        ]
        kb = inline.delete_award_kb(award_id=award_id)
        await callback.message.answer_photo(photo=award_profile["photo_id"], caption="\n".join(text), reply_markup=kb)
    else:
        text = "Что-то пошло не так 🤷"
        kb = inline.home_kb()
        await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "delete_award")
async def main_block(callback: CallbackQuery):
    award_id = int(callback.data.split(":")[1])
    award_profile = await AwardsDAO.get_one_or_none(id=award_id)
    if award_profile:
        text = f"Вознаграждение <i>{award_profile['title']}</i> успешно удалено"
        await AwardsDAO.delete(id=award_id)
    else:
        text = "Это вознаграждение было уже удалено ранее"
    kb = inline.home_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "add_award")
async def main_block(callback: CallbackQuery, state: FSMContext):
    award_type = callback.data.split(":")[1]
    text = "Введите название вознаграждения"
    kb = inline.home_kb()
    await state.set_state(AdminFSM.title_award)
    await state.update_data(award_type=award_type)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.message(F.text, AdminFSM.title_award)
async def main_block(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    text = "Введите описание приза (форматирование будет сохранено)"
    kb = inline.home_kb()
    await state.set_state(AdminFSM.description_award)
    await message.answer(text, reply_markup=kb)


@router.message(F.text, AdminFSM.description_award)
async def main_block(message: Message, state: FSMContext):
    await state.update_data(description=message.html_text)
    text = "Отправьте фото"
    kb = inline.home_kb()
    await state.set_state(AdminFSM.photo_award)
    await message.answer(text, reply_markup=kb)


@router.message(F.photo, AdminFSM.photo_award)
async def main_block(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    text = "Введите цену"
    kb = inline.home_kb()
    await state.set_state(AdminFSM.price_award)
    await message.answer(text, reply_markup=kb)


@router.message(F.text, AdminFSM.price_award)
async def main_block(message: Message, state: FSMContext):
    kb = inline.home_kb()
    try:
        price = int(message.text)
    except ValueError:
        text = "Нужно ввести число"
        await message.answer(text, reply_markup=kb)
        return
    state_data = await state.get_data()
    await AwardsDAO.create(type_award=state_data["award_type"],
                           title=state_data["title"],
                           description=state_data["description"],
                           photo_id=state_data["photo"],
                           price=price)
    text = "Вознаграждение создано"
    await message.answer(text, reply_markup=kb)
