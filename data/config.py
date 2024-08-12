BOT_TOKEN = '7127086448:AAHtK7EwqJ7rvpzGFMGp4BQZrFaIESR6nQU'
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
    'ask_phone_uz': "*Telefon raqamingizni yuboring*",
    'ask_phone_ru': "*Отправьте свой номер телефона*",
    'ask_phone_kr': "*Телефон рақамингизни юборинг*",
    'initial_uz': ['👤 Jismoniy shaxslar uchun', '🏢 Yuridik shaxslar uchun', '💱 Valyuta kursi va tarixi',
                   '📰 Yangiliklar', '🏠 Manzillar', '⚙️ Sozlamalar'],
    'initial_ru': ['👤 Для физических лиц', '🏢 Для юридических лиц', '💱 Курсы валют и история', '📰 Новости', '🏠 Адреса',
                   '⚙️ Настройки'],
    'initial_kr': ['👤 Жисмоний шахслар учун', '🏢 Юридик шахслар учун', '💱 Валюта курси ва тарихи', '📰 Янгиликлар',
                   '🏠 Манзиллар', '⚙️ Созламалар'],
    'mainM_uz' : ['💳 Kreditlar', '💰 Omonatlar', '💳 Bank Kartalar', '💸 To\'lovlar', '🛠️ Xizmatlar',
                '👶 Bola Puli Va Nafaqa', '💼 Xazna',
                '📞 Xalq Banki Raqamlari'],
}


