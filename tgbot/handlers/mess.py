from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline import personal_data_choice
from tgbot.misc.states import UsersStates
from tgbot.models.commands import get_or_create_user


async def mess(message: Message, state: FSMContext) -> None:
    """
    Хэндлер, реагирующий на команду /mess.
    Получает или создаёт пользователя и запрашивает подтвердить или ввести имя.
    """

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


def register_mess(dp: Dispatcher):
    dp.register_message_handler(mess, commands=["mess"], state="*"),
