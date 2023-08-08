from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для отправки своего контакта
share_phone = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Отправить свой номер телефона", request_contact=True)],
    ],
    one_time_keyboard=True
)
