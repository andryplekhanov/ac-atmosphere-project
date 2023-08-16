from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import main_categories_choice, categories_choice
from tgbot.misc.factories import for_cat
from tgbot.models.commands import get_categories, get_products


async def menu(message: Message, state: FSMContext) -> None:
    await state.finish()
    cats = await get_categories()
    async with state.proxy() as data:
        data['last_command'] = 'menu'
        data['categories'] = cats
    await message.answer(f'Выберите категорию', reply_markup=await main_categories_choice(cats))


async def get_category(call: CallbackQuery, state: FSMContext, callback_data: dict) -> None:
    await call.message.edit_reply_markup(reply_markup=None)

    cat_id = int(callback_data.get('category_id'))
    states = await state.get_data()
    all_cats = states.get('categories')
    sub_cats = {key: val for key, val in all_cats.items() if int(val.get('parent_id')) == cat_id}
    products = await get_products(cat_id)
    await call.message.answer(f'Выбирайте:', reply_markup=await categories_choice(sub_cats, products))

    await call.message.delete()


def register_menu(dp: Dispatcher):
    dp.register_message_handler(menu, commands=["menu"], state="*", is_banned=False)
    dp.register_callback_query_handler(get_category, for_cat.filter(), state="*", is_banned=False)
