from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.factories import for_answer

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


def answer_from_admin(user_id: str) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками для администратора - выбор действия с сообщением.
    """

    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(InlineKeyboardButton(
        text='Ответить',
        callback_data=for_answer.new(user_id=user_id, action='answer')
    ))
    keyboard.add(InlineKeyboardButton(
        text='Спам (блокировать)',
        callback_data=for_answer.new(user_id=user_id, action='spam')
    ))
    return keyboard
