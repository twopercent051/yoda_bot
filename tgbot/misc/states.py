from aiogram.fsm.state import State, StatesGroup


class AdminFSM(StatesGroup):
    home = State()
    title_award = State()
    description_award = State()
    photo_award = State()
    price_award = State()
