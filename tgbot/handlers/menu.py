from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import categories_choice
from tgbot.misc.factories import for_cat
from tgbot.models.commands import get_categories


async def menu(message: Message, state: FSMContext) -> None:
    await state.finish()
    async with state.proxy() as data:
        data['last_command'] = 'menu'
    cats = await get_categories()
    await message.answer(f'Выберите категорию', reply_markup=categories_choice(cats))


async def get_category(call: CallbackQuery, state: FSMContext, callback_data: dict) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        data['current_stage'] = 'category'
    cat_id = callback_data.get('category_id')
    await call.message.answer(f'{cat_id}')
    await call.message.delete()


def register_menu(dp: Dispatcher):
    dp.register_message_handler(menu, commands=["menu"], state="*", is_banned=False)
    dp.register_callback_query_handler(get_category, for_cat.filter(), state="*", is_banned=False)
