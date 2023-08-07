from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура с выбором действия
personal_data_choice = InlineKeyboardMarkup(
    row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text='Верно. Оставить заявку на звонок.', callback_data='confirm_pers_data')
        ],
        [
            InlineKeyboardButton(text='Изменить данные.', callback_data='change_pers_data')
        ],
    ]
)