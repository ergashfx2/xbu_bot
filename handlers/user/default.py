import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.default.default import lanM, contact
from keyboards.inline.Share import Share
from loader import dp, bot
from filters.private import IsPrivate
from states.states import UserRegister
from utils.db_api.sqlite import db
from utils.misc.speak import speak
from utils.misc.external import get_currency_rates
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentTypes, ReplyKeyboardRemove


@dp.message_handler(text=['📰 Новости', '📰 Янгиликлар', '📰 Yangiliklar'])
async def start(message: types.Message):
    text = db.select_every_day_text()
    await message.answer(speak(speak(text[1], cid=message.from_user.id), cid=message.from_user.id),
                         parse_mode='markdown')


@dp.message_handler(text=['💱 Курсы валют и история', '💱 Валюта курси ва тарихи', '💱 Valyuta kursi va tarixi'])
async def start(message: types.Message):
    text = db.select_every_day_text()
    await message.answer(speak(text[0], cid=message.from_user.id), parse_mode='markdown')


@dp.message_handler(text=['🏠 Manzillar', '🏠 Адреса', '🏠 Манзиллар'])
async def manzillar(message: types, state: FSMContext):
    await message.answer(speak("Hozirda turgan joylashuvingizni yuboring", cid=message.from_user.id), parse_mode='markdown',
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
                             [KeyboardButton(speak('📍 Manzilimni yuborish', cid=message.from_user.id),
                                             request_location=True)],
                             [KeyboardButton(speak("🔙 Ortga qaytish", cid=message.from_user.id))]
                         ]))
    await state.set_state('location')


from utils.misc.location import get_closest_location


@dp.message_handler(state='location', content_types=ContentTypes.LOCATION)
async def location(message: types, state: FSMContext):
    print(message.location)
    await message.answer('🔎')
    await message.answer(speak('*Eng yaqin manzil qidirilmoqda biroz kutib turing*', cid=message.from_user.id),
                         parse_mode='markdown')
    location = get_closest_location(message.location.latitude, message.location.longitude)
    time.sleep(3)
    await message.answer(speak(f"*📍 Manzil :* {location[0]}\n*🗓 Ish kunlari* : {location[1]}\n*☎️ Bog'lanish* : {location[2]}\n*🔎 Uzoqlik* : {int(location[4])} km", cid=message.from_user.id))
    await bot.send_location(chat_id=message.chat.id, latitude=location[5], longitude=location[6])
    await state.finish()

@dp.message_handler(text=['⚙️ Sozlamalar','⚙️ Созламалар','⚙️ Настройки'])
async def sozlamalar(message:types.Message, state: FSMContext):
    await message.answer(speak("*Nimani o'zgartirmoqchisiz ?*", cid=message.from_user.id), parse_mode='markdown',reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
        [KeyboardButton(speak("🇺🇿 🇷🇺 Tilni o'zgartirish", cid=message.from_user.id))],
        [KeyboardButton(speak("☎️ Raqamni o'zgartirish", cid=message.from_user.id))],
        [KeyboardButton(speak("🔙 Ortga qaytish", cid=message.from_user.id))]
    ]))

@dp.message_handler(text=["🇺🇿 🇷🇺 Tilni o'zgartirish",'🇺🇿 🇷🇺 Сменить язык',"🇺🇿 🇷🇺 Тилни о'згартириш"])
async def change_language(message:types.Message, state:FSMContext):
    await message.answer(speak('*Tilni tanlang*',cid=message.from_user.id,),reply_markup=lanM)
    await UserRegister.lan.set()

@dp.message_handler(text=["☎️ Рақамни о'згартириш","☎️ Raqamni o'zgartirish",'☎️ Сменить номер'])
async def change_phone(message:types.Message, state:FSMContext):
    await message.answer(speak('Telefon raqamingizni yuboring',cid=message.from_user.id),reply_markup=contact(cid=message.from_user.id))
    await UserRegister.phone.set()


