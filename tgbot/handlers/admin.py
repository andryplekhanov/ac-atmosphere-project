from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.default_commands import get_default_commands


async def admin_start(message: Message):
    commands = await get_default_commands()
    await message.answer(f"Привет и добро пожаловать!\n\n"
                         f"Я реагирую на следующие команды:\n\n{commands}")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
