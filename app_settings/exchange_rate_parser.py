import logging
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app_settings.models import CurrencySettings

logger = logging.getLogger(__name__)


def scrap_rate() -> Decimal:
    """
    Веб-скраппер. Забирает курс доллара к рублю с сайта google.ru.
    Если скраппинг не удался, возвращает 0.0
    """

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
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url=url, headers=headers)

    if response.status_code == 200:
        logger.info(f"Parsing ex rate: response.status_code == 200")
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            dollar_rate = soup.find_all('span', class_='DFlfde SwHCTb')[0]
            dollar_rate = dollar_rate.text.replace(',', '.')
            return Decimal.from_float(float(dollar_rate)).quantize(Decimal("1.00"))
        except Exception as ex:
            logger.error(f"Parsing ex rate: FAIL: {ex}")
            return Decimal.from_float(0.0).quantize(Decimal("1.00"))
    else:
        logger.error(f"Parsing ex rate: FAIL")
        return Decimal.from_float(0.0).quantize(Decimal("1.00"))


def get_exchange_rate():
    """
    Функция вызывает скраппер курса доллара (scrap_rate) и обновляет данные модели CurrencySettings.
    """

    exchange_rate = scrap_rate()
    try:
        CurrencySettings.objects.update_or_create(current_rate=exchange_rate)
    except Exception as ex:
        logger.error(f"get_exchange_rate: FAIL: {ex}")
