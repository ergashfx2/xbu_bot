import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import texts
from filters.admins import AdminFilter
from loader import bot, dp
from utils.db_api.sqlite import db
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.default import *
from states.states import UserRegister
from utils.misc.speak import speak, translate_menu
from utils.misc.twilio import send_sms
from states.states import MenuCustom
from keyboards.inline.chat import chat_btn

@dp.message_handler(state='*', text=['🔙 Ortga qaytish','🔙 Вернуться назад','🔙 Ортга қайтиш'])
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    
    await message.answer(
        speak('*Xush kelibsiz! Kerakli menyuni tanlang*', cid=message.from_user.id),
        reply_markup=generate_btn(
            btn_list=texts[f"initial_{db.select_user(cid=message.from_user.id)[3]}"],cid=1
        )
    )

@dp.message_handler(state='*',text=['📞 Ishonch raqami','📞 Ишонч рақами','📞 Доверительный номер','🏢 Yuridik shaxslar uchun','🏢 Для юридических лиц','🏢 Юридик шахслар учун'])
async def xalq_banki(message: types, state: FSMContext):
    text = """
    *☎️  Xalq Banki ishonch raqami: +998712102002*

📞  *Qisqa raqam* - 1106
    """
    await message.answer(text, parse_mode='Markdown')


@dp.message_handler(state='*',text=['💬 Chat','💬 Чат','💬 Чат'])
async def xalq_banki(message: types, state: FSMContext):
    text = """
    *Ushbu telegram orqali Xalq bankiga doir istalgan savolingizni yozib yuborishngiz mumkin. Operatorga savolingizni yozish uchun pastdagi tugmani bosing! 👇🏻*
    """
    await message.answer(speak(text,cid=message.from_user.id), parse_mode='Markdown',reply_markup=chat_btn)



@dp.message_handler(state='*',commands='start')
async def send(message: Message):
    user = db.select_user(cid=message.from_user.id)
    if user[3] and user[4] is not None:
        await message.answer(
            speak('*Xush kelibsiz! Kerakli menyuni tanlang*', cid=message.from_user.id),
            reply_markup=generate_btn(
                btn_list=texts[f"initial_{db.select_user(cid=message.from_user.id)[3]}"], cid=message.from_user.id
            )
        )
    else:
        await message.answer(
            "* 🇷🇺 Добро пожаловать! Выберите пожалуйста язык. \n\n 🇺🇿 Xush kelibsiz! Tilni tanlang.*",
            parse_mode="markdown", reply_markup=lanM
        )
        await UserRegister.lan.set()

@dp.message_handler(state=UserRegister.lan)
async def lan(message: Message, state: FSMContext):
    msg = message.text
    if msg == "🇺🇿 O'zbek":
        db.update_user(lan='uz', id=message.from_user.id)
        await message.answer(texts["ask_phone_uz"], parse_mode="Markdown", reply_markup=contact(cid=message.from_user.id))
    elif msg == '🇺🇿 ўзбек':
        db.update_user(lan='kr', id=message.from_user.id)
        await message.answer(texts["ask_phone_kr"], parse_mode="Markdown", reply_markup=contact(cid=message.from_user.id))
    elif msg == '🇷🇺 Русский':
        db.update_user(id=message.from_user.id, lan='ru')
        await message.answer(texts["ask_phone_ru"], parse_mode="Markdown", reply_markup=contact(cid=message.from_user.id))
    await UserRegister.phone.set()

@dp.message_handler(state=UserRegister.phone, content_types=['contact'])
async def phone(message: types.Message, state: FSMContext):
    phone = message.contact['phone_number']
    code = random.randint(1000, 9999)
    text = speak(f"Sizning tasdiqlash kodingiz {code}", cid=message.from_user.id)
    await state.update_data({'code': code})
    await state.update_data({'phone': phone})
    await message.answer(str(code), parse_mode="Markdown")
    await message.answer(
        speak(speak(text='*Telefon raqamingizga yuborilgan 4 xonali kodni yozing*', cid=message.from_user.id), cid=message.from_user.id), parse_mode='Markdown'
    )
    try:
        send_sms(phone=phone, message=text)
    except:
        pass
    await UserRegister.code.set()

@dp.message_handler(state=UserRegister.code)
async def code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    code = data.get('code')
    phone = data.get('phone')
    if str(code) == message.text:
        db.update_user(id=message.from_user.id, phone=phone)
        lan = db.select_user(cid=message.from_user.id)[3]
        menu_list = translate_menu(lan, texts['initial_uz'])
        await message.answer(
            speak('*Xush kelibsiz! Kerakli menyuni tanlang*', cid=message.from_user.id), parse_mode='Markdown',
            reply_markup=generate_btn(btn_list=menu_list, cid=message.from_user.id)
        )
        await state.finish()

@dp.message_handler(text=['👤 Для физических лиц', '👤 Jismoniy shaxslar uchun', '👤 Жисмоний шахслар учун'])
async def menu(message: types.Message, state: FSMContext):
    lan = db.select_user(cid=message.from_user.id)[3]
    menu_list = translate_menu(lan, texts['mainM_uz'])
    await message.answer(
        speak("*Jismoniy shaxslar bo'limiga xush kelibsiz! Kerakli menyuni tanlang*", cid=message.from_user.id), parse_mode='Markdown',
        reply_markup=generate_btn(btn_list=menu_list, cid=message.from_user.id)
    )
    await state.set_state('jismoniy_shaxslar')

@dp.message_handler(state='jismoniy_shaxslar')
async def jismoniy_shaxslar(message: types.Message, state: FSMContext):
    if message.text != speak('🔙 Ortga qaytish',cid=message.from_user.id):
        lan = db.select_user(cid=message.from_user.id)[3]
        btn_list = db.select_menu_buttons(menu=message.text, lan=lan)
        menus_list = [item[0] for item in btn_list]
        await message.answer(
            speak('Kerakli menyuni tanlang', cid=message.from_user.id), parse_mode='Markdown',
            reply_markup=generate_btn(menus_list, cid=message.from_user.id)
        )
        await state.set_state('jismoniy_buttons')

@dp.message_handler(state='jismoniy_buttons')
async def jismoniy_buttons(message: types.Message, state: FSMContext):
    lan = db.select_user(cid=message.from_user.id)[3]
    btn_list = db.select_menu_content(button_text=message.text, lan=lan)
    if btn_list[0]:
        await bot.copy_message(chat_id=message.chat.id, message_id=btn_list[0], from_chat_id='-1002205517577')
    else:
        await bot.send_message(chat_id=message.chat.id, text='*Hech nima topilmadi*')
