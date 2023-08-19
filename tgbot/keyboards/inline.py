from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.factories import for_cat, for_prod, for_back, for_order

# Клавиатура с выбором действия
personal_data_choice = InlineKeyboardMarkup(
    row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text='Верно', callback_data='confirm_pers_data')
        ],
        [
            InlineKeyboardButton(text='Изменить данные', callback_data='change_pers_data')
        ],
    ]
)


async def main_categories_choice(categories: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for cat_id, cat_data in categories.items():
        if cat_data.get('parent_id') == 0:
            keyboard.add(InlineKeyboardButton(
                text=f"👉 {cat_data.get('name')}",
                callback_data=for_cat.new(category_id=cat_id)
            ))
    return keyboard


async def categories_choice(categories: dict, products: dict, cat: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    if categories:
        for cat_id, cat_data in categories.items():
            keyboard.add(InlineKeyboardButton(
                text=f"👉 {cat_data.get('name')}",
                callback_data=for_cat.new(category_id=cat_id)
            ))
    if products:
        for prod_id, prod_data in products.items():
            keyboard.add(InlineKeyboardButton(
                text=f"{prod_data.get('title')} (💰 {prod_data.get('total_price')} руб.)",
                callback_data=for_prod.new(product_id=prod_id, prev_cat=cat)
            ))
    keyboard.add(InlineKeyboardButton(text=f"<< Назад", callback_data=for_back.new(prev_cat=cat, section='cat')))
    return keyboard


async def product_detail(prod_id: int, cat: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f"👍 Оставить заявку", callback_data=for_order.new(prod_id=prod_id)))
    keyboard.add(InlineKeyboardButton(text=f"<< Назад", callback_data=for_back.new(prev_cat=cat, section='prod')))
    return keyboard
