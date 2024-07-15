from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import texts
from filters.admins import AdminFilter
from loader import bot, dp
from utils.db_api.sqlite import db
from loader import dp
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton
from keyboards.default.default import *
from states.states import UserRegister
from utils.misc.speak import speak

@dp.message_handler(commands="start")
async def send(message: Message):
    user = db.select_user(cid=message.from_user.id)
    if user[3] and user[4] is not None:
        await message.answer(speak('*Xush kelibsiz ! Kerakli menyuni tanlang*',cid=message.from_user.id),reply_markup=generate_btn(lan=db.select_user(cid=message.from_user.id),btn_list=texts['mainM']))
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
        await message.answer(texts["ask_phone_uz"], parse_mode="Markdown", reply_markup=generate_btn(lan='uz',btn_list=["📞 Telefon raqamini yuborish"],contact=True))
    elif msg == '🇺🇿 ўзбек':
        db.update_user(lan='kr', id=message.from_user.id)
        await message.answer(texts["ask_phone_kr"], parse_mode="Markdown",reply_markup=generate_btn(lan='kr',btn_list=["📞 Telefon raqamini yuborish"],contact=True))
    elif msg == '🇷🇺 Русский':
        db.update_user(id=message.from_user.id, lan='ru')
        await message.answer(texts["ask_phone_ru"], parse_mode="Markdown",reply_markup=generate_btn(lan='ru',btn_list=["📞 Telefon raqamini yuborish"],contact=True))
    await UserRegister.phone.set()


@dp.message_handler(state=UserRegister.phone,content_types=['contact'])
async def phone(message: types.Message, state: FSMContext):
    db.update_user(phone=message.contact['phone_number'],id=message.from_user.id)
    await message.answer(speak('*Qabul qilindi*',cid=message.from_user.id),parse_mode='Markdown',reply_markup=generate_btn(lan=db.select_user(cid=message.from_user.id)[3],btn_list=texts['mainM']))
    await state.finish()
