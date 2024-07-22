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
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.firefox import GeckoDriverManager

def get_news():
    # Initialize Firefox options
    options = FirefoxOptions()
    
    # Set up a proxy if necessary
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = "localhost:8080"  # Adjust the proxy settings as needed
    proxy.ssl_proxy = "localhost:8080"
    
    # Adding proxy to Firefox options
    options.proxy = proxy

    # Initialize the Firefox driver with options
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=options
    )
    
    try:
        # Open the target page
        driver.get("https://xb.uz/post")

        # Find the element containing the news link and get the URL
        row_data = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div[1]/a')
        news_url = row_data.get_attribute('href')

        # Navigate to the news URL
        driver.get(news_url)

        # Find the element containing the news title
        row_data = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div/h2')
        news_title = row_data.text

        return f"*{news_title}*\n\n*Batafsil* :{news_url}"

    finally:
        # Close the browser
        driver.quit()

# Example usage
print(get_news())


