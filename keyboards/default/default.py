from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from deep_translator import GoogleTranslator
from utils.misc.translitrate import to_cyrillic
lanM = ReplyKeyboardMarkup(resize_keyboard=True)
lanM.add(KeyboardButton("🇺🇿 O'zbek"))
lanM.insert(KeyboardButton("🇷🇺 Русский"))
from utils.misc.speak import speak
def contact(cid):
    contact = ReplyKeyboardMarkup(resize_keyboard=True)
    contact.add(KeyboardButton(speak('📞 Telefon raqamim',cid=cid), request_contact=True))
    return contact



def generate_btn(btn_list,cid):
    lists = [item[0] for item in btn_list]
    print(btn_list)
    btns = ReplyKeyboardMarkup(resize_keyboard=True)
    for index, btn in enumerate(btn_list):
        if index % 2 == 0:
            btns.add(KeyboardButton(btn))
        else:
            btns.insert(KeyboardButton(btn))
    if cid != 1:
        btns.add(speak(text='🔙 Ortga qaytish',cid=cid))

    return btns
