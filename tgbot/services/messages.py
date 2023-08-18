import os
from typing import Union

from aiogram.types import Message, CallbackQuery, ChatActions, MediaGroup, InputFile

from dj_ac.settings import BASE_DIR
from tgbot.keyboards.inline import product_detail
from tgbot.models.commands import get_all_admins, get_product_detail


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
        await message.bot.send_contact(chat_id=admin_dict.get('tg_id'),
                                       first_name=fullname,
                                       phone_number=phone_number)


async def send_messages_new_mess(message: Message, user_fullname: str) -> None:
    """ Отпраляет сообщение с контактами администраторов """

    await message.answer(f'{user_fullname}, напишите ваше обращение администратору:')
    admins = await get_all_admins()
    for admin_dict in admins:
        await message.answer(f"{admin_dict.get('name')}\n@{admin_dict.get('username')}")


async def print_product_detail(message: Union[Message, CallbackQuery], prod_id: int, parent_id: int) -> None:
    """
    Печатает сообщение с детальной информацией о товаре и кнопками с возможностью заказать.
    """

    product = await get_product_detail(prod_id)
    text = (f"<b>{product.title}</b>\n\n"
            f"📦 Наличие: <code>{product.avaliable_status}</code>\n"
            f"💰 Цена: <code>{product.total_price} руб.</code>\n\n"
            f"<i>{product.description}</i>")

    if product.images.all():
        await message.edit_text('Загружаю фото...')
        await ChatActions.upload_photo()

        if len(product.images.all()) == 1:
            url = os.path.join(BASE_DIR, 'media', str(product.images.first().image))
            await message.bot.send_photo(chat_id=message.chat.id,
                                         photo=InputFile(url),
                                         caption=text,
                                         parse_mode='html',
                                         reply_markup=await product_detail(prod_id, parent_id))
        else:
            media = MediaGroup()
            for img in product.images.all():
                media.attach_photo(InputFile(os.path.join(BASE_DIR, 'media', str(img.image))))
            await message.bot.send_media_group(chat_id=message.chat.id, media=media)
            await message.answer(text, parse_mode='html', reply_markup=await product_detail(prod_id, parent_id))
    else:
        await message.answer(text, parse_mode='html', reply_markup=await product_detail(prod_id, parent_id))
