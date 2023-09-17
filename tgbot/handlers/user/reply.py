from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class UserReplyKeyboard:
    """Клавиатура юзера для передачи телефона"""

    def __init__(self):
        self.__home_button = KeyboardButton(text="В начало")

    @staticmethod
    def main_menu_kb():
        kb = [
            [
                KeyboardButton(text="💰 Узнать баланс"),
                KeyboardButton(text="💡 Обменять баллы"),
            ],
            [KeyboardButton(text="📝 Список вознаграждений")]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=False)

    def request_phone_kb(self):
        kb = [
            [
                KeyboardButton(text="Поделиться телефоном", request_contact=True),
                self.__home_button
            ]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=False)

    def awards_menu_kb(self):
        kb = [
            [
                KeyboardButton(text="Вознаграждения без списания баллов"),
                KeyboardButton(text="Вознаграждения со списанием баллов"),
            ],
            [self.__home_button]
        ]
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=False)
