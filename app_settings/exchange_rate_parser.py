from decimal import Decimal

import requests
from bs4 import BeautifulSoup


def scrap_rate() -> float:
    headers = {
        'authority': 'www.kith.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        'sec-fetch-dest': 'document',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'accept-language': 'en-US,en;q=0.9',
    }
    url = 'https://www.google.ru/search?q=dollar+rouble+rate'

    session = requests.session()
    response = session.get(url=url, headers=headers)

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            dollar_rate = soup.find_all('span', class_='DFlfde SwHCTb')[0]
            dollar_rate = dollar_rate.text.replace(',', '.')
            return float(dollar_rate)
        except Exception:
            return 0.0
    else:
        return 0.0


def get_exchange_rate():
    exchange_rate = scrap_rate()
    return Decimal.from_float(exchange_rate).quantize(Decimal("1.00"))
