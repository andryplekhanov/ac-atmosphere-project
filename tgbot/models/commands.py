# Не менять порядок импортов
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_ac.settings")
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
django.setup()

import logging

from typing import Union

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from app_telegram.models import TGUser, CallRequest


logger = logging.getLogger(__name__)


@sync_to_async
def find_user(user_id: int) -> Union[TGUser, None]:
    """ Ищет пользователя в БД. Возвращает объект пользователя либо None. """

    try:
        user = TGUser.objects.get(tg_id=user_id)
        logger.info(f"user {user_id} was found in DB")
        return user
    except ObjectDoesNotExist as ex:
        logger.info(f"FAIL. User {user_id} was NOT found in DB: {ex}")
        return None


@sync_to_async
def add_or_get_user(user_id: int, full_name: str, username: str, phone: str) -> TGUser:
    """ Создаёт нового пользователя в БД. Возвращает объект пользователя. """

    user, created = TGUser.objects.get_or_create(tg_id=user_id)
    if created:
        logger.info(f"user {user_id} was added to DB")
    user.username = username
    user.fullname = full_name
    user.phone_number = phone
    user.save()
    return user


@sync_to_async
def add_call_request(user: TGUser) -> Union[CallRequest, None]:
    """ Создаёт заявку на звонок. Возвращает объект CallRequest или False. """

    try:
        call = CallRequest.objects.create(from_user=user)
        logger.info(f"CallRequest from {user} was added to DB")
        return call
    except Exception as ex:
        logger.error(f"FAIL. CallRequest from {user} was NOT added to DB: {ex}")
        return None
