from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from deep_translator import GoogleTranslator
from utils.misc.translitrate import to_cyrillic
lanM = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
lanM.add(KeyboardButton("🇺🇿 O'zbek"))
lanM.insert(KeyboardButton("🇺🇿 ўзбек"))
lanM.insert(KeyboardButton("🇷🇺 Русский"))

contact = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
contact.add(KeyboardButton('Telefon raqam', request_contact=True))


def generate_btn(btn_list):
    btns = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for index, btn in enumerate(btn_list):
        if index % 2 == 0:
            btns.add(KeyboardButton(btn))
        else:
            btns.insert(KeyboardButton(btn))

    return btns
