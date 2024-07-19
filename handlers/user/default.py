from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.Share import Share
from loader import dp, bot
from filters.private import IsPrivate
from utils.db_api.sqlite import db
from utils.misc.speak import speak
from utils.misc.utils import get_currency_rates

@dp.message_handler(text=['📰 Новости','📰 Янгиликлар','📰 Yangiliklar'])
async def start(message: types.Message):
    lan = db.select_user(cid=message.from_user.id)[3]


@dp.message_handler(text=['💱 Курсы валют и история','💱 Валюта курси ва тарихи','💱 Valyuta kursi va tarixi'])
async def start(message: types.Message):
    lan = db.select_user(cid=message.from_user.id)[3]
    rates = get_currency_rates()
    await message.answer(speak(rates,cid=message.from_user.id),parse_mode='markdown')

