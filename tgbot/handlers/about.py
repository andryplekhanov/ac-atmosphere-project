from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.commands import get_company_info
from tgbot.services.default_commands import get_default_commands


async def about(message: Message, state: FSMContext) -> None:
    """
    Хендлер, реагирующий на команду /about.
    Получает из БД информацию о компании и выводит её.
    """

    await state.finish()
    info = await get_company_info()
    email = f'email: {info.email}' if info.email else ''
    phone_number = f'телефон: {info.phone_number}' if info.phone_number else ''
    phone_messengers = f'телефон (мессенджеры): {info.phone_messengers}' if info.phone_messengers else ''
    description = f'{info.description}' if info.description else ''

    await message.answer(f"<b>{info.company}</b>\n\n"
                         f"<i>{description}</i>\n\n"
                         f"<b>Контакты:</b><code>\n{email}\n{phone_number}\n{phone_messengers}</code>\n\n"
                         f"Связаться с нами можно прямо через данного бота. Жмите команду:\n"
                         f"<b>/call</b> - заказать обратный звонок;\n"
                         f"<b>/mess</b> - написать нам текстовое сообщение\n\n")


def register_about(dp: Dispatcher):
    dp.register_message_handler(about, commands=["about"], state="*", is_banned=False)
