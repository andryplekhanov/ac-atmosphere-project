from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.db.models import QuerySet

from tgbot.misc.factories import for_cat

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


def categories_choice(categories: QuerySet) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for category in categories:
        if not category.parent:
            keyboard.add(InlineKeyboardButton(
                text=f'👉 {category.name}',
                callback_data=for_cat.new(category_id=category.id)
            ))
    return keyboard
