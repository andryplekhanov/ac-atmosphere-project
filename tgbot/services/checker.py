import re

from typing import Union

from aiogram.types import Message


async def check_phone(message: Message) -> Union[str, None]:
    """ Функция проверяет телефон на валидность """

    phone_number = None
    if message.text:
        is_phone_valid = re.fullmatch(r'^\+\d{11,20}', message.text)
        if not is_phone_valid:
            await message.answer('Номер телефона должен быть в формате +79012345678')
        else:
            phone_number = message.text
    elif message.contact.phone_number:
        phone_number = message.contact.phone_number
        phone_number = '+' + phone_number

    return phone_number
