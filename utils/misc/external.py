import datetime
import requests
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

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
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from browsermobproxy import Server

def get_news():
    # Start the BrowserMob Proxy server
    server = Server("browsermob-proxy")
    server.start()
    proxy = server.create_proxy()
    
    # Set up Chrome options to use the proxy
    chrome_options = Options()
    chrome_options.add_argument(f"--proxy-server={proxy.proxy}")

    # Initialize the WebDriver with the Chrome options
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    # Set up the request header modification
    proxy.headers({'Host': '*'})
    
    driver.get("https://xb.uz/post")

    row_data = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div[1]/a')
    news_url = row_data.get_attribute('href')
    driver.get(news_url)
    row_data = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div/h2')
    news_title = row_data.text

    # Stop the proxy server
    server.stop()

    driver.quit()

    return f"*{news_title}*\n\n*Batafsil* :{news_url}"

# Usage
print(get_news())



