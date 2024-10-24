from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    phone_number = State()
