import datetime
import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_news():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://xb.uz/post")

    try:
        # Wait for the element to be present
        wait = WebDriverWait(driver, 10)
        row_data = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div[1]/a')))
        news_url = row_data.get_attribute('href')

        driver.get(news_url)

        row_data = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div/h2')))
        news_title = row_data.text

        return f"*{news_title}*\n\n*Batafsil* :{news_url}"
    finally:
        driver.quit()


if __name__ == "__main__":
    print(get_news())




