# Не менять порядок импортов
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_ac.settings")
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
django.setup()

import logging
from typing import Union

from asgiref.sync import sync_to_async
from django.db.models import QuerySet

from app_products.models import Category, Product
from app_settings.models import AdminItem
from app_telegram.models import TGUser, CallRequest

logger = logging.getLogger(__name__)


@sync_to_async
def get_or_create_user(user_id: int) -> TGUser:
    """ Создаёт нового пользователя в БД или возвращает существующего. Возвращает объект пользователя. """

    user, created = TGUser.objects.get_or_create(tg_id=user_id)
    if created:
        logger.info(f"user {user_id} was added to DB")
        user.fullname = 'не заполнено'
        user.phone_number = 'не заполнено'
        user.save()
    return user


@sync_to_async
def update_user(user_id: int, full_name: str, phone: str) -> TGUser:
    """ Обновляет данные пользователя в БД. Возвращает объект пользователя. """

    user = TGUser.objects.get(tg_id=user_id)
    user.fullname = full_name
    user.phone_number = phone
    user.save()
    logger.info(f"{user} was updated in DB")
    return user


@sync_to_async
def add_call_request(user_id: int) -> Union[CallRequest, None]:
    """ Создаёт заявку на звонок. Возвращает объект CallRequest или None. """

    try:
        user = TGUser.objects.get(tg_id=user_id)
        call = CallRequest.objects.create(from_user=user)
        logger.info(f"CallRequest from {user} was added to DB")
        return call
    except Exception as ex:
        logger.error(f"FAIL. CallRequest from {user} was NOT added to DB: {ex}")
        return None


@sync_to_async
def get_all_admins() -> list[dict]:
    """
    Получает всех админов из модели AdminItem.
    Возвращает список словарей. Каждый элемент списка - словарь с данными админа.
    """

    admins = AdminItem.objects.all()
    result = list()
    for admin in admins:
        admin_dict = dict()
        admin_dict['name'] = admin.name
        admin_dict['phone_number'] = admin.phone_number
        admin_dict['tg_id'] = admin.tg_id
        admin_dict['username'] = admin.username
        result.append(admin_dict)
    return result


@sync_to_async
def get_banned_ids() -> list[int]:
    """
    Получает всех забаненных пользователей.
    Возвращает список идентификаторов.
    """

    banned_users = TGUser.objects.filter(is_banned=True).only('tg_id')
    return [user.tg_id for user in banned_users]


@sync_to_async
def get_categories() -> dict:
    """
    Получает все категории товаров.
    Возвращает dict с категориями.
    """

    result = dict()
    cats = Category.objects.all()
    for cat in cats:
        cat_id = cat.id
        cat_name = cat.name
        cat_parent_id = 0 if not cat.parent else cat.parent.id
        result[cat_id] = {'name': cat_name, 'parent_id': cat_parent_id}
    return result


@sync_to_async
def get_products(cat_id: int) -> dict:
    """
    Получает продукты указанной категории (cat_id).
    Возвращает dict с продуктами.
    """

    result = dict()
    products = Product.objects.select_related('category').filter(category_id=cat_id).exclude(available='no')
    for prod in products:
        prod_id = prod.id
        prod_title = prod.title
        prod_total_price = prod.total_price
        prod_parent_id = prod.category.id
        result[prod_id] = {
            'title': prod_title,
            'total_price': prod_total_price,
            'parent_id': prod_parent_id
        }
    return result
