import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import texts
from filters.admins import AdminFilter
from loader import bot, dp
from utils.db_api.sqlite import db
from loader import dp
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.default import *
from states.states import UserRegister
from utils.misc.speak import speak
from utils.misc.twilio import send_sms


@dp.message_handler(commands="start")
async def send(message: Message):
    user = db.select_user(cid=message.from_user.id)
    if user[3] and user[4] is not None:
        await message.answer(speak('*Xush kelibsiz ! Kerakli menyuni tanlang*', cid=message.from_user.id),
                             reply_markup=generate_btn(
                                 btn_list=texts[f"initial_{db.select_user(cid=message.from_user.id)[3]}"]))
    else:
        await message.answer(
            "* 🇷🇺 Добро пожаловать! Выберите пожалуйста язык. \n\n 🇺🇿 Xush kelibsiz! Tilni tanlang.*",
            parse_mode="markdown", reply_markup=lanM)
        await UserRegister.lan.set()


@dp.message_handler(state=UserRegister.lan)
async def lan(message: Message, state: FSMContext):
    msg = message.text
    if msg == "🇺🇿 O'zbek":
        db.update_user(lan='uz', id=message.from_user.id)
        await message.answer(texts["ask_phone_uz"], parse_mode="Markdown", reply_markup=contact)
    elif msg == '🇺🇿 ўзбек':
        db.update_user(lan='kr', id=message.from_user.id)
        await message.answer(texts["ask_phone_kr"], parse_mode="Markdown", reply_markup=contact)
    elif msg == '🇷🇺 Русский':
        db.update_user(id=message.from_user.id, lan='ru')
        await message.answer(texts["ask_phone_ru"], parse_mode="Markdown", reply_markup=contact)
    await UserRegister.phone.set()


@dp.message_handler(state=UserRegister.phone, content_types=['contact'])
async def phone(message: types.Message, state: FSMContext):
    phone = message.contact['phone_number']
    code = random.randint(1000, 9999)
    text = speak(f"Sizning tasdiqlash kodingiz {code}", cid=message.from_user.id)
    send_sms(phone_number=phone, message=text)
    await state.update_data({'code': code})
    await state.update_data({'phone': phone})
    await message.answer(
        speak(speak(text='*Telefon raqamingizga yuborilgan 4 xonali kodni yozing*', cid=message.from_user.id),
              cid=message.from_user.id), parse_mode='Markdown')
    await UserRegister.code.set()


@dp.message_handler(state=UserRegister.code)
async def code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    code = data.get('code')
    print(code)
    print(message.text)
    phone = data.get('phone')
    if str(code) == message.text:
        print('working')
        db.update_user(id=message.from_user.id, phone=phone)
        await message.answer(speak('*Xush kelibsiz ! Kerakli menyuni tanlang*', cid=message.from_user.id), parse_mode='Markdown',reply_markup=generate_btn(btn_list=texts[f"inital_{db.select_user(cid=message.from_user.id)[3]}"]))
        await state.finish()

@dp.message_handler(text=['👤 Для физических лиц','👤 Jismoniy shaxslar uchun','👤 Жисмоний шахслар учун'])
async def menu(message: types.Message):
    await message.answer(speak("*Jismoniy shaxslar bo'limiga xush kelibsiz ! Kerakli menyuni tanlang*", cid=message.from_user.id), parse_mode='Markdown',reply_markup=generate_btn(btn_list=texts[f"mainM_{db.select_user(cid=message.from_user.id)[3]}"]))