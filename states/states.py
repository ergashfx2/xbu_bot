from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegister(StatesGroup):
    lan = State()
    phone = State()
