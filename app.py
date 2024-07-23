import asyncio
import logging

from aiogram import executor
from loader import dp
import middlewares, filters, handlers

from utils.db_api.sqlite import db
from utils.misc.external import get_currency_rates, get_news



logging.basicConfig(level=logging.INFO)

async def job():
    try:
        logging.info("Fetching currency rates...")
        currency_rates = get_currency_rates()
        logging.info("Fetching news...")
        news = get_news()
        logging.info("Updating database...")
        db.add_every_day_text(currency_rates, news)
        logging.info("Database updated.")
    except Exception as e:
        logging.error(f"Error in job: {e}")

async def periodic_job(interval):
    while True:
        await job()
        await asyncio.sleep(interval)

async def on_startup(dispatcher):
    logging.info("Starting periodic job...")
    asyncio.create_task(periodic_job(25200))

if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
