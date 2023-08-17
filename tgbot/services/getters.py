from aiogram.dispatcher import FSMContext

from tgbot.models.commands import get_products


async def get_subcats_and_products(cat_id: int, state: FSMContext) -> tuple[dict, dict]:
    """
    Берет все категории из машины состояний и фильтрует в словарь: выбирает подкатегории указанной категории cat_id.
    Получает список продуктов указанной категории.
    Возвращает словарь с подкатегориями и словарь с продуктами.
    """

    states = await state.get_data()
    all_cats = states.get('categories')

    sub_cats = {key: val for key, val in all_cats.items() if int(val.get('parent_id')) == cat_id}
    products = await get_products(cat_id)

    return sub_cats, products


async def get_parent_id(current_cat: int, state: FSMContext) -> int:
    """
    Берет все категории из машины состояний и ищет из них родителя указанной категории current_cat.
    """

    states = await state.get_data()
    all_cats = states.get('categories')
    parent_id = all_cats.get(str(current_cat)).get('parent_id')
    return int(parent_id)
