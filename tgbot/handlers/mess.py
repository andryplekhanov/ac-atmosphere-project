from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.config import Config
from tgbot.keyboards.inline import personal_data_choice
from tgbot.misc.states import UsersStates
from tgbot.models.commands import get_or_create_user, update_user
from tgbot.services.saver import save_message


async def mess(message: Message, state: FSMContext) -> None:
    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'mess'
        data['user_id'] = int(message.from_user.id)

    user = await get_or_create_user(user_id=int(message.from_user.id))
    if user.fullname == 'не заполнено':
        await message.answer('Введите ваше имя')
        await UsersStates.user_fullname.set()
    else:
        async with state.proxy() as data:
            data['user_phone'] = user.phone_number
            data['user_fullname'] = user.fullname
        await message.answer(f'Ваше имя: <b>{user.fullname}</b>\n'
                             f'💡 Верно?',
                             reply_markup=personal_data_choice, parse_mode='html')


async def get_text_mess(message: Message, state: FSMContext, config: Config) -> None:
    async with state.proxy() as data:
        data['user_message'] = message.text
    states = await state.get_data()
    phone = 'не заполнено' if states.get('user_phone') == 'не заполнено' else states.get('user_phone')
    user = await update_user(user_id=states.get('user_id'), full_name=states.get('user_fullname'), phone=phone)
    await save_message(user, message, state, config)


def register_mess(dp: Dispatcher):
    dp.register_message_handler(mess, commands=["mess"], state="*"),
    dp.register_message_handler(get_text_mess, state=UsersStates.user_message),
