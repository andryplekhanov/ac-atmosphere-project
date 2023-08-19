# Не менять порядок импортов...
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_ac.settings")
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
django.setup()
# ... до сюда.

import logging
from typing import Union

from asgiref.sync import sync_to_async

from app_orders.models import Order, OrderItem
from app_products.models import Category, Product
from app_settings.models import AdminItem, CompanySettings
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
def add_order(user_id: int, product_id: int, address: str) -> Union[Order, None]:
    """ Создаёт заказ. Возвращает объект Order или None. """

    try:
        user = TGUser.objects.get(tg_id=user_id)
        order = Order.objects.create(user=user, address=address)
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(order=order, product=product, price=product.total_price)
        logger.info(f"Order from {user} was added to DB")
        return order
    except Exception as ex:
        logger.error(f"FAIL. Order from {user} was NOT added to DB: {ex}")
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
def get_company_info() -> CompanySettings:
    """
    Получает информацию о компании из БД.
    Возвращает экземпляр класса CompanySettings.
    """

    return CompanySettings.objects.first()


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
    Получает все категории товаров. Возвращает dict с категориями.
    """

    result = dict()
    cats = Category.objects.all()
    for cat in cats:
        cat_parent_id = 0 if not cat.parent else cat.parent.id
        result[cat.id] = {'name': cat.name, 'parent_id': cat_parent_id}
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
        result[prod.id] = {
            'title': prod.title,
            'total_price': prod.total_price,
            'parent_id': prod.category.id
        }
    return result


@sync_to_async
def get_product_detail(prod_id: int) -> dict:
    """
    Получает продукты указанной категории (cat_id).
    Возвращает dict с продуктами.
    """

    product = Product.objects.get(id=prod_id)
    # logger.info(f"product {product.images.all()}")
    return product
