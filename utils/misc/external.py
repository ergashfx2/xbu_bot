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
    rates = f"*{'-'.join(date_today)}* kuni bo'yicha Xalq bankidagi valyuta kurslari\n\n"
    data = extract_currency_rates(cleaned_elements)
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


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_news():
    chromeOptions = webdriver.Options() 
    chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
    chromeOptions.add_argument("--no-sandbox") 
    chromeOptions.add_argument("--disable-setuid-sandbox") 
    chromeOptions.add_argument("--remote-debugging-port=9222")  # this
    chromeOptions.add_argument("--disable-dev-shm-using") 
    chromeOptions.add_argument("--disable-extensions") 
    chromeOptions.add_argument("--disable-gpu") 
    chromeOptions.add_argument("start-maximized") 
    chromeOptions.add_argument("disable-infobars")
    chromeOptions.add_argument(r"user-data-dir=.\cookies\\test")
    s = Service(r"/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=s,options=chromeOptions)

    try:
        driver.get("https://xb.uz/post")

        row_data = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div[1]/a')
        news_url = row_data.getAttribute('href')
        driver.get(news_url)

        row_data = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div/h2')
        news_title = row_data.text

        return f"*{news_title}*\n\n*Batafsil* :{news_url}"
    finally:
        driver.quit()

