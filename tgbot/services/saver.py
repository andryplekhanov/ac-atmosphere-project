from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app_telegram.models import TGUser
from tgbot.config import Config
from tgbot.models.commands import add_call_request
from tgbot.services.messages import send_messages_new_call_request


async def save_call_request(user: TGUser, message: Message, state: FSMContext, config: Config) -> None:
    call_request = await add_call_request(user=user)
    if call_request:
        await send_messages_new_call_request(message, config.tg_bot.admin_ids, user.fullname, user.phone_number,
                                             call_request.id)
    else:
        await message.answer('Произошла ошибка. Попробуйте ввести команду /call ещё раз')
    await state.reset_state(with_data=False)


