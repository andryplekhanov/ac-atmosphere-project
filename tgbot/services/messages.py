from aiogram.types import Message


async def send_messages_new_call_request(message: Message,
                                         admins: list,
                                         fullname: str,
                                         phone_number: str,
                                         call_request_id: int
                                         ) -> None:
    """ Отправляет сообщения об успешной заявке на звонок пользователю и админам бота. """

    await message.answer(f'👍 {fullname}, заявка №{call_request_id} успешно создана.\n'
                         f'Ожидайте звонка на номер {phone_number}.',
                         parse_mode='html')

    for admin_id in admins:
        await message.bot.send_message(chat_id=admin_id,
                                       text=f'<b>🔥 Уведомление для администратора!</b>\n'
                                            f'Новая заявка на звонок №{call_request_id}:\n\n'
                                            f'<code>{fullname}\n'
                                            f'{phone_number}</code>\n\n'
                                            f'<i>Заявка сохранена в базе. '
                                            f'Рекомендуется зайти в админ-панель и отметить её статус, '
                                            f'чтобы она не затерялась.</i>',
                                       parse_mode='html'
                                       )


async def send_messages_new_mess(message: Message,
                                 admins: list,
                                 fullname: str,
                                 phone_number: str,
                                 mess_id: int,
                                 mess_text: str
                                 ) -> None:
    """ Отправляет сообщения об успешном создании обращения пользователю и админам бота. """

    await message.answer(f'👍 {fullname}, обращение №{mess_id} успешно создано.\n'
                         f'Мы вскоре с вами свяжемся.',
                         parse_mode='html')

    # for admin_id in admins:
    #     if not username == 'nousername':
    #         text = (f'<b>🔥 Уведомление для администратора!</b>\nНовое обращение №{mess_id}:\n'
    #                 f'<code>Имя: {fullname}\nТекст сообщения:\n{mess_text}</code>\n'
    #                 f'Чтобы ответить на сообщение, позвоните по номеру <b>{phone_number}</b> '
    #                 f'или напишите пользователю в личной переписке (нажмите @{username}).\n\n'
    #                 f'<i>Обращение сохранено в базе. Рекомендуется зайти в админ-панель и отметить его статус, '
    #                 f'чтобы оно не затерялось.</i>')
    #     else:
    #         text = (f'<b>🔥 Уведомление для администратора!</b>\nНовое обращение №{mess_id}:\n'
    #                 f'<code>Имя: {fullname}\nТекст сообщения:\n{mess_text}</code>\n'
    #                 f'Чтобы ответить на сообщение, позвоните по номеру <b>{phone_number}</b>.\n\n'
    #                 f'<i>Обращение сохранено в базе. Рекомендуется зайти в админ-панель и отметить его статус, '
    #                 f'чтобы оно не затерялось.</i>')
    #     await message.bot.send_message(chat_id=admin_id, text=text, parse_mode='html')
