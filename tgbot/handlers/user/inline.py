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
    def awards_menu_kb():
        keyboard = [
            [InlineKeyboardButton(text="📝 Список вознаграждений", callback_data="get_awards")],
            [InlineKeyboardButton(text="💡 Обменять баллы", callback_data="withdrawal_balance")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

