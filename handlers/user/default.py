import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.locations import create_locations_button
from keyboards.default.default import lanM, contact
from keyboards.inline.Share import Share
from loader import dp, bot
from filters.private import IsPrivate
from states.states import UserRegister
from utils.db_api.sqlite import db
from utils.misc.speak import speak
from utils.misc.external import get_currency_rates
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentTypes, ReplyKeyboardRemove


@dp.message_handler(state='*',text=['📰 Новости', '📰 Янгиликлар', '📰 Yangiliklar'])
async def start(message: types.Message):
    text = db.select_every_day_text()
    await message.answer(speak(speak(text[1], cid=message.from_user.id), cid=message.from_user.id),
                         parse_mode='markdown')


@dp.message_handler(state='*',text=['💱 Курс валют', '💱 Валюта курси ва тарихи', '💱 Valyuta kursi'])
async def start(message: types.Message):
    text = db.select_every_day_currency()
    print(text)
    await message.answer(speak(text[0], cid=message.from_user.id), parse_mode='markdown')


@dp.message_handler(state='*',text=['🏠 Manzillar', '🏠 Адреса', '🏠 Манзиллар'])
async def manzillar(message: types, state: FSMContext):
    await message.answer(speak('*Kerakli menyuni tanlang*',cid=message.from_user.id),parse_mode='markdown',reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
        [KeyboardButton(text=speak('📍 Barcha manzillar',cid=message.from_user.id))],
        [KeyboardButton(text=speak('🔍 Eng yaqin manzilni topish',cid=message.from_user.id))],
        [KeyboardButton(text=speak('🔙 Ortga qaytish',cid=message.from_user.id))]
    ]))
    await state.set_state('locations')


@dp.message_handler(state='locations',text=['📍 Barcha manzillar','📍Все адреса'])
async def all_locations(msg: types.Message, state: FSMContext):
    locations = db.select_locations_viloyat()
    string_list = await convert_string_list(locations)
    await msg.answer(speak("*Viloyatingizni tanlang*",cid=msg.from_user.id),reply_markup=create_locations_button(string_list))
    await state.set_state('locations_viloyat')


@dp.message_handler(state='locations',text=['🔍 Eng yaqin manzilni topish','🔍 Найдите ближайший адрес'])
async def all_locations(msg: types.Message, state: FSMContext):
    await msg.answer(speak("*Manzilingizni yuboring*",cid=msg.from_user.id),reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
        [KeyboardButton(speak('📍 Manzilimni yuborish',cid=msg.from_user.id),request_location=True)],
        [KeyboardButton(text=speak('🔙 Ortga qaytish',cid=msg.from_user.id))]
    ]))
    await state.set_state('location')



@dp.callback_query_handler(state='locations_viloyat')
async def viloyat(msg:types.CallbackQuery,state:FSMContext):
    tumanlar = db.select_location_tuman(viloyat=msg.data)
    print(tumanlar)
    string_list = await convert_string_list(tumanlar)
    await msg.message.edit_text(speak("*Tumaningizni tanlang*",cid=msg.from_user.id),reply_markup=create_locations_button(string_list))
    await state.set_state('locations_tuman')


@dp.callback_query_handler(state='locations_tuman')
async def viloyat(msg:types.CallbackQuery,state:FSMContext):
    bxmlar = db.select_location_bxm(tuman=msg.data)
    string_list = await convert_string_list(bxmlar)
    await msg.message.edit_text(speak("*Filialni tanlang*",cid=msg.from_user.id),reply_markup=create_locations_button(string_list))
    await state.set_state('locations_bxm')


@dp.callback_query_handler(state='locations_bxm')
async def viloyat(msg:types.CallbackQuery,state:FSMContext):
    print(msg.data)
    coordinates = await convert_string_list(db.select_location_coordinates(bxm=msg.data))
    print(coordinates)
    try:
        lat,long = str(coordinates[0]).split(',')
    except:
        lat,long = str(coordinates[0]).split(' ')
    await msg.message.edit_text(speak('*Ushbu filialning manzilini yuboryapman...*',cid=msg.from_user.id),parse_mode='markdown')
    await msg.message.answer_location(latitude=lat,longitude=long)
    await state.set_state('locations')


from utils.misc.location import get_closest_location


@dp.message_handler(state='location', content_types=ContentTypes.LOCATION)
async def location(message: types, state: FSMContext):
    print(message.location)
    await message.answer('🔎')
    await message.answer(speak('*Eng yaqin manzil qidirilmoqda biroz kutib turing*', cid=message.from_user.id),
                         parse_mode='markdown')
    location = get_closest_location(message.location.latitude, message.location.longitude)
    time.sleep(2)
    await message.answer(speak(f"*📍 Manzil :* {location[4]}\n*🗓 Ish kunlari* : \n\n{location[3]}\n", cid=message.from_user.id))
    lat,long = str(location[5]).split(',') 
    await bot.send_location(chat_id=message.chat.id, latitude=lat, longitude=long)
    await state.finish()

@dp.message_handler(state='*',text=['⚙️ Sozlamalar','⚙️ Созламалар','⚙️ Настройки'])
async def sozlamalar(message:types.Message, state: FSMContext):
    await message.answer(speak("*Nimani o'zgartirmoqchisiz ?*", cid=message.from_user.id), parse_mode='markdown',reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
        [KeyboardButton(speak("🇺🇿 🇷🇺 Tilni o'zgartirish", cid=message.from_user.id))],
        [KeyboardButton(speak("☎️ Raqamni o'zgartirish", cid=message.from_user.id))],
        [KeyboardButton(speak("🔙 Ortga qaytish", cid=message.from_user.id))]
    ]))

@dp.message_handler(state='*',text=["🇺🇿 🇷🇺 Tilni o'zgartirish",'🇺🇿 🇷🇺 Сменить язык',"🇺🇿 🇷🇺 Тилни о'згартириш"])
async def change_language(message:types.Message, state:FSMContext):
    await message.answer(speak('*Tilni tanlang*',cid=message.from_user.id,),reply_markup=lanM)
    await UserRegister.lan.set()

@dp.message_handler(state='*',text=["☎️ Рақамни о'згартириш","☎️ Raqamni o'zgartirish",'☎️ Сменить номер'])
async def change_phone(message:types.Message, state:FSMContext):
    await message.answer(speak('Telefon raqamingizni yuboring',cid=message.from_user.id),reply_markup=contact(cid=message.from_user.id))
    await UserRegister.phone.set()


async def convert_string_list(list):
    return [item[0] for item in list]