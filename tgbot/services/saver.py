from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from app_telegram.models import TGUser
from tgbot.models.commands import add_call_request, update_user
from tgbot.services.messages import send_messages_new_call_request, send_messages_new_mess


async def save_call_request(user: TGUser, message: Union[Message, CallbackQuery], state: FSMContext) -> None:
    """
    Функция-обработчик.
    Вызывает функцию, создающую новую заявку на звонок (add_call_request).
    Если заявка была успешно создана, вызывает функцию, отправляющую сообщения (send_messages_new_call_request).
    """

    call_request = await add_call_request(user=user)
    if call_request:
        await send_messages_new_call_request(message, user.fullname, user.phone_number, call_request.id)
    else:
        await message.answer('Произошла ошибка. Попробуйте ввести команду /call ещё раз')
    await state.reset_state(with_data=False)


async def save_message(message: Union[Message, CallbackQuery], state: FSMContext) -> None:
    """
     Функция-обработчик.
     Вызывает функцию, обновляющую модель пользователя (update_user).
     Затем вызывает функцию, отправляющую сообщения (send_messages_new_mess).
     """

    states = await state.get_data()

    phone = 'не заполнено' if states.get('user_phone') == 'не заполнено' else states.get('user_phone')
    user = await update_user(user_id=states.get('user_id'), full_name=states.get('user_fullname'), phone=phone)

    await send_messages_new_mess(message=message, user_fullname=user.fullname)
    await state.reset_state(with_data=False)
