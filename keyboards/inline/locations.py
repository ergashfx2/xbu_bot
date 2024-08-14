from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


def create_locations_button(list):
    keyb = InlineKeyboardMarkup()
    index = 0
    for btn in list:
        if index % 2 == 0:
            keyb.add(InlineKeyboardButton(text=btn,callback_data=btn))
            index += 1
        else:
            keyb.insert(InlineKeyboardButton(btn,callback_data=btn))
            index += 1
    return keyb
