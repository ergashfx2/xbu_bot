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
from states.states import MenuCustom

@dp.message_handler(state=[MenuCustom.menu,MenuCustom.buttons,MenuCustom.button_ru,MenuCustom.button_uz,MenuCustom.button_kr,MenuCustom.content_uz,MenuCustom.content_ru,MenuCustom.content_kr], commands=['start'])
async def start(message:types.Message, state:FSMContext):
    await state.finish()
    await message.answer(speak('*Xush kelibsiz ! Kerakli menyuni tanlang*', cid=message.from_user.id),
                         reply_markup=generate_btn(
                             btn_list=texts[f"initial_{db.select_user(cid=message.from_user.id)[3]}"]))

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
    send_sms(phone=phone, message=text)
    await state.update_data({'code': code})
    await state.update_data({'phone': phone})
    await message.answer(str(code), parse_mode="Markdown")
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
async def menu(message: types.Message, state: FSMContext):
    await message.answer(speak("*Jismoniy shaxslar bo'limiga xush kelibsiz ! Kerakli menyuni tanlang*", cid=message.from_user.id), parse_mode='Markdown',reply_markup=generate_btn(btn_list=texts[f"mainM_{db.select_user(cid=message.from_user.id)[3]}"]))
    await state.set_state('jismoniy_shaxslar')

@dp.message_handler(state='jismoniy_shaxslar')
async def jismoniy_shaxslar(message: types.Message, state: FSMContext):
    btn_list = db.select_menu_buttons(menu=message.text)
    menus_list = [item[0] for item in btn_list]
    await message.answer(speak('Kerakli menyuni tanlang', cid=message.from_user.id), parse_mode='Markdown',reply_markup=generate_btn(menus_list))
    await state.set_state('jismoniy_buttons')

@dp.message_handler(state='jismoniy_buttons')
async def jismoniy_buttons(message: types.Message, state: FSMContext):
    lan = db.select_user(cid=message.from_user.id)[3]
    print(lan)
    btn_list = db.select_menu_content(button_text=message.text,lan=lan)
    await bot.copy_message(chat_id=message.chat.id, message_id=btn_list[0][0], from_chat_id='-1002243641076')

