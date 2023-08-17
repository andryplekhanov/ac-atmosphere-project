from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import main_categories_choice, categories_choice
from tgbot.misc.factories import for_cat, for_back, for_prod
from tgbot.models.commands import get_categories
from tgbot.services.getters import get_subcats_and_products, get_parent_id
from tgbot.services.messages import print_product_detail


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
    sub_cats, products = await get_subcats_and_products(cat_id=cat_id, state=state)
    await call.message.answer(f'Выбирайте:', reply_markup=await categories_choice(sub_cats, products, cat_id))

    await call.message.delete()


async def get_back(call: CallbackQuery, state: FSMContext, callback_data: dict) -> None:
    await call.message.edit_reply_markup(reply_markup=None)

    cat_id = int(callback_data.get('prev_cat'))
    parent_id = await get_parent_id(current_cat=cat_id, state=state)
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
    await call.message.edit_reply_markup(reply_markup=None)

    prod_id = int(callback_data.get('product_id'))
    await print_product_detail(message=call.message, prod_id=prod_id)

    await call.message.delete()


def register_menu(dp: Dispatcher):
    dp.register_message_handler(menu, commands=["menu"], state="*", is_banned=False)
    dp.register_callback_query_handler(get_category, for_cat.filter(), state="*", is_banned=False)
    dp.register_callback_query_handler(get_back, for_back.filter(), state="*")
    dp.register_callback_query_handler(get_product_detail, for_prod.filter(), state="*")