from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.services.default_commands import get_default_commands


async def help(message: Message, state: FSMContext) -> None:
    await state.finish()
    commands = await get_default_commands()
    await message.answer(f"Я реагирую на следующие команды:\n\n{commands}")


def register_help(dp: Dispatcher):
    dp.register_message_handler(help, commands=["help"], state="*", is_banned=False)
