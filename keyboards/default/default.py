from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from deep_translator import GoogleTranslator
from utils.misc.translitrate import to_cyrillic
lanM = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
lanM.add(KeyboardButton("🇺🇿 O'zbek"))
lanM.insert(KeyboardButton("🇺🇿 ўзбек"))
lanM.insert(KeyboardButton("🇷🇺 Русский"))

contact = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
contact.add(KeyboardButton('Telefon raqam', request_contact=True))

def generate_btn(lan, btn_list,contact=None):
    btns = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    count = 1
    if lan != 'kr':
        translator = GoogleTranslator(source='auto', target=lan)
    for btn in btn_list:
        btn = btn.title()
        if count % 2 == 0:
            if contact is not None:
                if lan != 'kr':
                    btns.insert(KeyboardButton(translator.translate(btn, dest=lan), request_contact=True))
                else:
                    btns.insert(KeyboardButton(to_cyrillic(btn),request_contact=True))
                count += 1
            else:
                if lan != 'kr':
                    btns.insert(KeyboardButton(translator.translate(btn, dest=lan)))
                else:
                    btns.insert(KeyboardButton(to_cyrillic(btn)))
                count += 1
        else:
            if contact is not None:
                if lan != 'kr':
                    btns.add(KeyboardButton(translator.translate(btn, dest=lan),request_contact=True))
                else:
                    btns.add(KeyboardButton(to_cyrillic(btn),request_contact=True))
                count += 1
            else:
                if lan != 'kr':
                    btns.add(KeyboardButton(translator.translate(btn, dest=lan)))
                else:
                    btns.add(KeyboardButton(to_cyrillic(btn)))
                count += 1
    return btns
