from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class InlineKeyboard:

    def __init__(self):
        self._home_button = InlineKeyboardButton(text="🏡 На главную", callback_data="home")

    def home_kb(self):
        keyboard = [[self._home_button]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @staticmethod
    def main_menu_kb():
        keyboard = [[InlineKeyboardButton(text="📝 Редактура призов", callback_data="edit_awards")]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def awards_list_kb(self, awards: List[dict]):
        keyboard = []
        for award in awards:
            keyboard.append([InlineKeyboardButton(text=award["title"], callback_data=f"award:{award['id']}")])
        keyboard.append([InlineKeyboardButton(text="➕ Добавить награду со списанием",
                                              callback_data="add_award:with_write_downs")])
        keyboard.append([InlineKeyboardButton(text="➕ Добавить награду без списания",
                                              callback_data="add_award:without_write_downs")])
        keyboard.append([self._home_button])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def delete_award_kb(self, award_id: str | int):
        keyboard = [
            [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_award:{award_id}")],
            [self._home_button]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
