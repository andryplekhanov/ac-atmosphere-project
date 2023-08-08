from aiogram import types, Dispatcher


async def ban_all(message: types.Message):
    await message.answer('🛑 Вы внесены в чёрный список!')


def register_ban(dp: Dispatcher):
    dp.register_message_handler(ban_all, state="*", content_types=types.ContentTypes.ANY, is_banned=True)
