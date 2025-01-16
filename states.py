from aiogram.fsm.state import State, StatesGroup


class MenuSG(StatesGroup):
    photo_and_location = State()
    payment = State()
