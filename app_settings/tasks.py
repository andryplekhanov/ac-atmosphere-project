import logging

from app_settings.exchange_rate_parser import get_exchange_rate
from dj_ac.celery import app

logger = logging.getLogger(__name__)


@app.task
def get_rate():
    """ Таск по обновлению курса доллара """

    try:
        logger.info(f"Starting task 'get_rate'")
        get_exchange_rate()
    except Exception as ex:
        logger.error(f"get_exchange_rate: FAIL: {ex}")
        pass
    