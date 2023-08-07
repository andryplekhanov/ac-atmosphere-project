from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from app_telegram.models import TGUser
from tgbot.config import Config
from tgbot.models.commands import add_call_request, add_message
from tgbot.services.messages import send_messages_new_call_request, send_messages_new_mess


async def save_call_request(
        user: TGUser,
        message: Union[Message, CallbackQuery],
        state: FSMContext,
        config: Config) -> None:
    """
    aaa
    """

    call_request = await add_call_request(user=user)
    if call_request:
        await send_messages_new_call_request(message, config.tg_bot.admin_ids, user.fullname, user.phone_number,
                                             call_request.id)
    else:
        await message.answer('Произошла ошибка. Попробуйте ввести команду /call ещё раз')
    await state.reset_state(with_data=False)


async def save_message(user: TGUser, message: Message, state: FSMContext, config: Config) -> None:
    """
    fff
    """

    states = await state.get_data()
    mess = await add_message(user=user, text=states.get('user_message'))
    if mess:
        await send_messages_new_mess(message, config.tg_bot.admin_ids, user.fullname, user.phone_number, mess.id, mess.text)
    else:
        await message.answer('Произошла ошибка. Попробуйте ввести команду /mess ещё раз')
    await state.reset_state(with_data=False)
