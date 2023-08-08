from aiogram.types import Message

from tgbot.models.commands import get_all_admins


async def send_messages_new_call_request(message: Message, fullname: str,
                                         phone_number: str, call_request_id: int) -> None:
    """ Отправляет сообщения об успешной заявке на звонок пользователю и админам бота. """

    await message.answer(f'👍 {fullname}, заявка №{call_request_id} успешно создана.\n'
                         f'Ожидайте звонка на номер {phone_number}.',
                         parse_mode='html')

    admins = await get_all_admins()
    for admin_dict in admins:
        await message.bot.send_message(chat_id=admin_dict.get('tg_id'),
                                       text=f'<b>🔥 Уведомление для администратора!</b>\n'
                                            f'Новая заявка на звонок №{call_request_id}:\n\n'
                                            f'<code>{fullname}\n'
                                            f'{phone_number}</code>\n\n'
                                            f'<i>Заявка сохранена в базе. '
                                            f'Рекомендуется зайти в админ-панель и отметить её статус, '
                                            f'чтобы она не затерялась.</i>',
                                       parse_mode='html'
                                       )


async def send_messages_new_mess(message: Message, user_fullname: str) -> None:
    """ Отпраляет сообщение с контактами администраторов """

    await message.answer(f'{user_fullname}, напишите ваше обращение администратору:')
    admins = await get_all_admins()
    for admin_dict in admins:
        await message.answer(f"{admin_dict.get('name')}\n@{admin_dict.get('username')}")
