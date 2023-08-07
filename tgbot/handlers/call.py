import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config
from tgbot.keyboards.inline import personal_data_choice
from tgbot.misc.states import UsersStates
from tgbot.models.commands import add_or_get_user, find_user
from tgbot.services.saver import save_call_request


async def call(message: Message, state: FSMContext) -> None:
    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'call'

    user = await find_user(user_id=int(message.from_user.id))
    if user:
        async with state.proxy() as data:
            data['user'] = user
        await message.answer(f'Ваше имя: <b>{user.fullname}</b>\n'
                             f'Ваш телефон: <b>{user.phone_number}</b>\n'
                             f'💡 Всё верно?',
                             reply_markup=personal_data_choice, parse_mode='html')
    else:
        await message.answer('Введите ваше имя')
        await UsersStates.user_fullname.set()


async def change_personal_data(call: CallbackQuery) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Введите ваше имя')
    await UsersStates.user_fullname.set()


async def confirm_personal_data(call: CallbackQuery, state: FSMContext, config: Config) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    states = await state.get_data()
    await save_call_request(user=states.get('user'), message=call.message, state=state, config=config)


async def get_fullname(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['user_fullname'] = message.text
        data['user_id'] = int(message.from_user.id)
        data['user_username'] = message.from_user.username
    await message.answer('Введите номер телефона в формате +79012345678')
    await UsersStates.user_phone.set()


async def get_phone(message: Message, state: FSMContext, config: Config) -> None:
    is_phone_valid = re.fullmatch(r'^\+\d{11,20}', message.text)
    if not is_phone_valid:
        await message.answer('Номер телефона должен быть в формате +79012345678')
    else:
        async with state.proxy() as data:
            data['user_phone'] = message.text
        states = await state.get_data()
        user = await add_or_get_user(user_id=states.get('user_id'),
                                     full_name=states.get('user_fullname'),
                                     username=states.get('user_username'),
                                     phone=states.get('user_phone')
                                     )
        await save_call_request(user, message, state, config)


def register_call(dp: Dispatcher):
    dp.register_message_handler(call, commands=["call"], state="*"),
    dp.register_message_handler(get_fullname, state=UsersStates.user_fullname),
    dp.register_message_handler(get_phone, state=UsersStates.user_phone, content_types=['contact', 'text']),
    dp.register_callback_query_handler(change_personal_data, text='change_pers_data', state="*")
    dp.register_callback_query_handler(confirm_personal_data, text='confirm_pers_data', state="*")
