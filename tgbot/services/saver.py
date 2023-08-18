from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.models.commands import add_call_request, update_user
from tgbot.services.messages import send_messages_new_call_request, send_messages_new_mess


async def save_call_request(message: Union[Message, CallbackQuery], state: FSMContext) -> None:
    """
    Функция-обработчик.
    Вызывает функцию, создающую новую заявку на звонок (add_call_request).
    Если заявка была успешно создана, вызывает функцию, отправляющую сообщения (send_messages_new_call_request).
    """

    states = await state.get_data()

    call_request = await add_call_request(user_id=states.get('user_id'))
    if call_request:
        await send_messages_new_call_request(message, states.get('user_fullname'), states.get('user_phone'),
                                             call_request.id)
    else:
        await message.answer('Произошла ошибка. Попробуйте ввести команду /call ещё раз')
    await state.reset_state(with_data=False)


async def save_order(message: Union[Message, CallbackQuery], state: FSMContext) -> None:
    """
    Функция-обработчик.
    Вызывает функцию, создающую новый заказ (add_order).
    Если заказ был успешно создан, вызывает функцию, отправляющую сообщения (send_messages_new_order).
    """

    states = await state.get_data()
    product_id = states.get('product_id')
    user_id = states.get('user_id')
    await message.answer(f'product_id {product_id} user_id {user_id}')

    # call_request = await add_call_request(user_id=states.get('user_id'))
    # if call_request:
    #     await send_messages_new_call_request(message, states.get('user_fullname'), states.get('user_phone'),
    #                                          call_request.id)
    # else:
    #     await message.answer('Произошла ошибка. Попробуйте ввести команду /menu ещё раз')
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
