import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_ac.settings")
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
django.setup()

import logging

from asgiref.sync import sync_to_async
from aiogram.dispatcher import FSMContext
from app_telegram.models import TGUser, CallRequest

logger = logging.getLogger(__name__)


@sync_to_async
def add_user(user_id, full_name, username):
    try:
        user = TGUser(tg_id=int(user_id), fullname=full_name, username=username).save()
        logger.info(f"user {user_id} was added to DB")
        return TGUser.objects.filter(tg_id=user_id).first()
    except Exception as ex:
        logger.error(f"FAIL. User {user_id} was NOT added to DB: {ex}")
        return TGUser.objects.filter(tg_id=user_id).first()


@sync_to_async
def add_call_request(user: TGUser, states: dict) -> bool:
    try:
        CallRequest(from_user=user, message=states.get('user_message')).save()
        logger.info(f"CallRequest from {user} was added to DB")
        return True
    except Exception as ex:
        logger.error(f"FAIL. User {user} was NOT added to DB: {ex}")
        return False
