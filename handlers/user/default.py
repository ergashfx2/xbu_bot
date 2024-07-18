from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.Share import Share
from loader import dp, bot
from filters.private import IsPrivate
from utils.db_api.sqlite import db


@dp.message_handler(text=['📰 Новости','📰 Янгиликлар','📰 Yangiliklar'])
async def start(message: types.Message):
    lan = db.select_user(cid=message.from_user.id)[3]
    btn_list = db.select_menu_content(button_text=message.text, lan=lan)
    if btn_list:
        await bot.copy_message(chat_id=message.chat.id, message_id=btn_list[0], from_chat_id='-1002243641076')
    else:
        await bot.send_message(chat_id=message.chat.id, text='*Hech nima topilmadi*')

