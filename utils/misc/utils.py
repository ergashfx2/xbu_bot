import datetime

import requests
from bs4 import BeautifulSoup

def extract_currency_rates(data):
    rates = {}
    i = 0
    while i < len(data):
            if data[i] == 'Valyuta':
                currency = data[i + 1]
                buy_rate = data[i + 3]
                sell_rate = data[i + 5]
                rates[currency] = {
                    'Sotib olish': buy_rate,
                    'Sotish': sell_rate
                }
            i += 1
    return rates


def get_currency_rates():
    url = "https://bank.uz/uz/currency/bank/xalq-bank"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'lxml')
    elements = soup.find_all('span', class_='medium-text')

    data = {}

    cleaned_elements = [element.get_text(strip=True) for element in elements if element.get_text(strip=True)]
    date_today = str(datetime.date.today()).split('-')[::-1]
    rates = f"*{'-'.join(date_today)}* kuni bo'yicha Xalq bankidagi valyura kurslari\n\n"
    data = extract_currency_rates(cleaned_elements)
    print(data)
    stickers = {
        'Evro': '💶',
        'AQSH dollari': '💵',
        'Angliya funt sterlingi': '💷',
        'Shveytsariya franki': '🇨🇭',
        'Qozog\'iston tengesi': '🇰🇿'
    }

    for currency in data:
        if currency == 'Sotib olish':
            continue
        emoji = stickers.get(currency, '')
        rates += f"{emoji} *{currency} kurslari*\n\n• *Sotib olish:* {data[currency]['Sotib olish']} So'm\n• *Sotish:* {data[currency]['Sotish']} So'm\n\n"

    return rates


def get_news():
    news_url = 'https://xb.uz/post'
    r = requests.get(news_url).content
    soup = BeautifulSoup(r, 'html.parser')
    search_word = 'post'

    # Find all elements with an href attribute
    for tag in soup.find_all(href=True):
        href = tag.get('href')
        print(href)

get_news()