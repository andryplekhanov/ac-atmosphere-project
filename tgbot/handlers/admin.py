from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from tgbot.misc.factories import for_answer
from tgbot.config import Config


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


async def get_action(call: CallbackQuery, callback_data: dict, state: FSMContext, config: Config):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(f"{callback_data.get('user_id')}, {callback_data.get('action')}")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_callback_query_handler(get_action, for_answer.filter(), state="*", is_admin=True),
