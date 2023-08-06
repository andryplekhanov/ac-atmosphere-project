from aiogram.types import Message


async def send_messages_new_call_request(message: Message,
                                        admins: list,
                                        fullname: str,
                                        phone_number: str,
                                        call_request_id: int) -> None:
    """ Отправляет сообщения об успешной заявке на звонок пользователю и админам бота. """

    await message.answer(f'👍 {fullname}, заявка №{call_request_id} успешно создана.\n'
                         f'Ожидайте звонка на номер {phone_number}.',
                         parse_mode='html')

    for admin_id in admins:
        await message.bot.send_message(chat_id=admin_id,
                                       text=f'<b>🔥 Уведомление для администратора!</b>\n'
                                            f'Новая заявка на звонок №{call_request_id}:\n'
                                            f'<code>{fullname}\n'
                                            f'{phone_number}</code>\n'
                                            f'<i>Заявка сохранена в базе. '
                                            f'Рекомендуется зайти в админ-панель и отметить её статус, '
                                            f'чтобы она не затерялась.</i>',
                                       parse_mode='html'
                                       )
