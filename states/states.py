from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegister(StatesGroup):
    lan = State()
    phone = State()
    code = State()


class MenuCustom(StatesGroup):
    menu = State()
    buttons = State()
    button_uz = State()
    button_ru = State()
    button_kr = State()
    content_uz = State()
    content_ru = State()
    content_kr = State()