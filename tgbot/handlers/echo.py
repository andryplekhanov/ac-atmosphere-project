from aiogram import types, Dispatcher

from tgbot.services.default_commands import get_default_commands


async def bot_echo(message: types.Message):
    commands = await get_default_commands()
    await message.answer(f"Я реагирую на следующие команды:\n\n{commands}")


async def bot_echo_all(message: types.Message):
    text = [
        f'Вы ввели что-то непонятное\n',
        'Пожалуйста, введите корректный ответ на вопрос, либо сбросьте состояние командой /start и начните заново.'
    ]
    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo, is_banned=False)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY, is_banned=False)
