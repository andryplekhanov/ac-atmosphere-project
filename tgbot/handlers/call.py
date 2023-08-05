from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import UsersStates
from tgbot.models.commands import add_user, add_call_request


async def call(message: Message, state: FSMContext) -> None:
    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'call'
    await message.answer('Введите ФИО')
    await UsersStates.user_fullname.set()


async def get_fullname(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['user_username'] = message.text
        data['user_id'] = int(message.from_user.id)
        data['user_username'] = message.from_user.username
    await message.answer('Введите номер телефона в формате +79012345678')
    await UsersStates.user_phone.set()


async def get_phone(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['user_phone'] = message.text
    await message.answer('Введите сообщение для администратора')
    await UsersStates.user_message.set()


async def get_message(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['user_message'] = message.text
    user = await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    states = await state.get_data()
    call_request = await add_call_request(user, states)
    if call_request:
        await message.answer('Заявка отправлена. Ожидайте звонка.')
    else:
        await message.answer('Произошла ошибка. Попробуйте ввести команду /call ещё раз')
    await state.reset_state(with_data=False)


def register_call(dp: Dispatcher):
    dp.register_message_handler(call, commands=["call"], state="*"),
    dp.register_message_handler(get_fullname, state=UsersStates.user_fullname),
    dp.register_message_handler(get_phone, state=UsersStates.user_phone),
    dp.register_message_handler(get_message, state=UsersStates.user_message),
