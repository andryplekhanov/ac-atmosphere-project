from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import personal_data_choice
from tgbot.keyboards.reply import share_phone
from tgbot.misc.states import UsersStates, ProductStates
from tgbot.models.commands import get_or_create_user, update_user
from tgbot.services.checker import check_phone
from tgbot.services.saver import save_call_request, save_message


async def call(message: Message, state: FSMContext) -> None:
    """
    Хэндлер, реагирующий на команду /call.
    Получает или создаёт пользователя и запрашивает подтвердить или ввести имя.
    """

    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'call'
        data['user_id'] = int(message.from_user.id)

    user = await get_or_create_user(user_id=int(message.from_user.id))
    if user.fullname == 'не заполнено' or user.phone_number == 'не заполнено':
        await message.answer('Введите ваше имя')
        await UsersStates.user_fullname.set()
    else:
        async with state.proxy() as data:
            data['user_fullname'] = user.fullname
            data['user_phone'] = user.phone_number
        await message.answer(f'Ваше имя: <b>{user.fullname}</b>\n'
                             f'Ваш телефон: <b>{user.phone_number}</b>\n'
                             f'💡 Всё верно?',
                             reply_markup=personal_data_choice, parse_mode='html')


async def change_personal_data(call: CallbackQuery) -> None:
    """
    Хэндлер, реагирующий на нажатие кнопки 'Изменить данные'.
    Запрашивает ввод имени.
    """

    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Введите ваше имя')
    await UsersStates.user_fullname.set()


async def confirm_personal_data(call: CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер, реагирующий на нажатие кнопки с подтверждением контактных данных.
    Проверяет последнюю введенную команду и вызывает соответствующую функцию-обработчик:
    save_call_request - если была введена команда /call;
    save_message - если была введена команда /mess
    продолжает опрос - если была введена команда /menu
    """

    await call.message.edit_reply_markup(reply_markup=None)
    states = await state.get_data()
    try:
        if states.get('last_command') == 'call':
            await save_call_request(message=call.message, state=state)
        elif states.get('last_command') == 'mess':
            await save_message(call.message, state)
        elif states.get('last_command') == 'menu':
            await ProductStates.address.set()
            await call.message.answer('Введите адрес доставки')
    except Exception:
        await state.finish()
        await call.message.answer('🚫 <b>Что-то пошло не так.</b> Возможно, вы не ввели контактные данные.\n'
                                  'Нажмите команду <b>/start</b> и попробуйте еще раз.', parse_mode='html')


async def get_fullname(message: Message, state: FSMContext) -> None:
    """
    Хэндлер, реагирующий на ввод имени.
    Записывает имя в состояние пользователя и проверяет последнюю введенную команду.
    Если была введена команда /mess - вызывает функцию-обработчик save_message,
    иначе запрашивает у пользователя телефон.
    """

    async with state.proxy() as data:
        data['user_fullname'] = message.text

    states = await state.get_data()
    if states.get('last_command') == 'mess':
        await save_message(message, state)
    else:
        await message.answer('Введите номер телефона в формате +79012345678\nили нажмите кнопку внизу',
                             reply_markup=share_phone)
        await UsersStates.user_phone.set()


async def get_phone(message: Message, state: FSMContext) -> None:
    """
    Хэндлер, реагирующий на ввод телефона. Проверяет функцией "check_phone" введённый телефон на валидность.
    Записывает телефон в состояние пользователя, обновляет данные в модели пользователя (update_user).
    Если была введена команда /call - вызывает функцию-обработчик save_call_request.
    Если была введена команда /menu - продолжает опрос.
    """

    phone_number = await check_phone(message)

    if phone_number:
        async with state.proxy() as data:
            data['user_phone'] = phone_number
        states = await state.get_data()
        await update_user(user_id=states.get('user_id'),
                          full_name=states.get('user_fullname'),
                          phone=states.get('user_phone'))

        states = await state.get_data()
        if states.get('last_command') == 'call':
            await save_call_request(message, state)
        elif states.get('last_command') == 'menu':
            await ProductStates.address.set()
            await message.answer('Введите адрес доставки')


def register_call(dp: Dispatcher):
    dp.register_message_handler(call, commands=["call"], state="*", is_banned=False),
    dp.register_message_handler(get_fullname, state=UsersStates.user_fullname),
    dp.register_message_handler(get_phone, state=UsersStates.user_phone, content_types=['contact', 'text'], is_banned=False),
    dp.register_callback_query_handler(change_personal_data, text='change_pers_data', state="*"),
    dp.register_callback_query_handler(confirm_personal_data, text='confirm_pers_data', state="*", is_banned=False)
