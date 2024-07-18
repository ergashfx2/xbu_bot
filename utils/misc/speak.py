import logging

from loader import bot
from utils.db_api.sqlite import db
from deep_translator import GoogleTranslator
from utils.misc.translitrate import to_cyrillic


def speak(text, cid):
    user = db.select_user(cid=cid)
    if user[3] == 'uz':
        return text
    elif user[3] == 'ru':
        return GoogleTranslator(source='auto', target='ru').translate(text)
    else:
        return to_cyrillic(text)


def translate_menu(lan,array=[]):
    text = ",".join(array)
    if lan == 'ru':
        translator = GoogleTranslator(source='auto', target='ru')
        return translator.translate(text).split(',')
    elif lan == 'kr':
        return to_cyrillic(text).split(',')
    else:
        return array

