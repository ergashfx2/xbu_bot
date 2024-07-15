BOT_TOKEN = '5228072940:AAEI7BTLr8nQrnCw6KHD9zCaQe5D_kQyK0E'
from utils.db_api.sqlite import db

admins = db.select_all_adminss()
channels = db.select_all_channel()
id_list = [id[0] for id in channels]
CHANNELS = list(map(lambda x: x[0], channels))

ids = [id[0] for id in admins]
ADMINS = list(map(lambda x: x[0], admins))
texts = db.select_all_from_texts()

Button_text = [texts[0][1]]
Text_caption = [texts[0][0]]

btns = {
    "accept": "Tekshirish",
    "back": "Ortga qaytish",
}

texts = {
    "text_to_start": f"<b>Assalomu alaykum! Botimizdan foydalanish uchun quyidagi kanallarga obuna bo'lishingiz kerak</b>",
    "main_menu": "Iltimos quyidagi menulardan birini tanlang!",
    "notaccepted": "❌<b> Quyidagi kanallarga a'zo bo'lmadingiz</b>, iltimos botdan foydalanish uchun kanalga a'zo bo'ling!",
    "accepted": "*Salom men orqali osongina konspekt qila olasiz shunchaki menga matn yuboring*",
    'ask_phone_uz':"*Telefon raqamingizni yuboring*",
    'ask_phone_ru':"*Отправьте свой номер телефона*",
    'ask_phone_kr':"*Телефон рақамингизни юборинг*",
    'mainM':['kreditlar','omonatlar','bank kartalar',"to'lovlar",'xizmatlar','bola puli va nafaqa','xazna','sozlamalar','yangiliklar','manzillar','Xalq banki raqamlari']
}