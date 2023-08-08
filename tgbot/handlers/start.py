from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def start(message: Message, state: FSMContext) -> None:
    await state.finish()
    await message.answer(f'hello')


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*", is_banned=False)
