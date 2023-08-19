from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import main_categories_choice, categories_choice, personal_data_choice
from tgbot.misc.factories import for_cat, for_back, for_prod, for_order
from tgbot.misc.states import UsersStates, ProductStates
from tgbot.models.commands import get_categories, get_or_create_user
from tgbot.services.getters import get_subcats_and_products, get_parent_id
from tgbot.services.messages import print_product_detail
from tgbot.services.saver import save_order


async def menu(message: Message, state: FSMContext) -> None:
    """
    Хэндлер, реагирующий на команду /menu.
    Получает все категории товаров и сохраняет их в машину состояний.
    Предлагает пользователя инлайн-клавиатуру с главными категориями.
    """

    await state.finish()
    cats = await get_categories()
    async with state.proxy() as data:
        data['user_id'] = int(message.from_user.id)
        data['last_command'] = 'menu'
        data['categories'] = cats
    await message.answer(f'Выберите категорию', reply_markup=await main_categories_choice(cats))


async def get_category(call: CallbackQuery, state: FSMContext, callback_data: dict) -> None:
    """
    Хэндлер, реагирующий на нажатие кнопки с категориями.
    Предлагает пользователя инлайн-клавиатуру с подкатегориями и товарами.
    """

    await call.message.edit_reply_markup(reply_markup=None)

    cat_id = int(callback_data.get('category_id'))
    sub_cats, products = await get_subcats_and_products(cat_id=cat_id, state=state)
    await call.message.answer(f'Выбирайте:', reply_markup=await categories_choice(sub_cats, products, cat_id))

    await call.message.delete()


async def get_back(call: CallbackQuery, state: FSMContext, callback_data: dict) -> None:
    """
    Хэндлер, реагирующий на нажатие кнопки "назад".
    Возвращает пользователя в предыдущее меню.
    """

    await call.message.edit_reply_markup(reply_markup=None)

    cat_id = int(callback_data.get('prev_cat'))
    if callback_data.get('section') == 'cat':
        parent_id = await get_parent_id(current_cat=cat_id, state=state)
    else:
        parent_id = cat_id

    if parent_id == 0:
        states = await state.get_data()
        cats = states.get('categories')
        await call.message.answer(f'Выберите категорию', reply_markup=await main_categories_choice(cats))
    else:
        sub_cats, products = await get_subcats_and_products(cat_id=parent_id, state=state)
        await call.message.answer(f'Выбирайте:',
                                  reply_markup=await categories_choice(sub_cats, products, parent_id))

    await call.message.delete()


async def get_product_detail(call: CallbackQuery, state: FSMContext, callback_data: dict) -> None:
    """
    Хэндлер, реагирующий на нажатие кнопки с конкретным товаром.
    Вызывает функцию для печати детальной информации по товару (print_product_detail).
    """

    await call.message.edit_reply_markup(reply_markup=None)

    prod_id = int(callback_data.get('product_id'))
    cat_id = int(callback_data.get('prev_cat'))
    await print_product_detail(message=call.message, prod_id=prod_id, parent_id=cat_id)

    await call.message.delete()


async def make_order(call: CallbackQuery, state: FSMContext, callback_data: dict) -> None:
    """
    Хэндлер, реагирующий на нажатие кнопки "оставить заявку" на конкретном товаре.
    Получает или создаёт пользователя и запрашивает подтвердить или ввести имя..
    """

    await call.message.edit_reply_markup(reply_markup=None)

    async with state.proxy() as data:
        data['product_id'] = int(callback_data.get('prod_id'))
        data['last_command'] = 'menu'

    states = await state.get_data()

    user = await get_or_create_user(user_id=states.get('user_id'))
    if user.fullname == 'не заполнено' or user.phone_number == 'не заполнено':
        await call.message.answer('Введите ваше имя')
        await UsersStates.user_fullname.set()
    else:
        async with state.proxy() as data:
            data['user_fullname'] = user.fullname
            data['user_phone'] = user.phone_number
        await call.message.answer(f'Ваше имя: <b>{user.fullname}</b>\n'
                                  f'Ваш телефон: <b>{user.phone_number}</b>\n'
                                  f'💡 Всё верно?',
                                  reply_markup=personal_data_choice, parse_mode='html')

    # await call.message.delete()


async def get_address(message: Message, state: FSMContext):
    """
    Хэндлер, реагирующий на состояние address.
    Получает адрес для доставки и вызывает функцию-обработчик для создания заказа.
    """

    async with state.proxy() as data:
        data['address'] = message.text
    await save_order(message, state)


def register_menu(dp: Dispatcher):
    dp.register_message_handler(menu, commands=["menu"], state="*", is_banned=False)
    dp.register_message_handler(get_address, state=ProductStates.address, is_banned=False)
    dp.register_callback_query_handler(get_category, for_cat.filter(), state="*")
    dp.register_callback_query_handler(get_back, for_back.filter(), state="*")
    dp.register_callback_query_handler(get_product_detail, for_prod.filter(), state="*")
    dp.register_callback_query_handler(make_order, for_order.filter(), state="*", is_banned=False)
