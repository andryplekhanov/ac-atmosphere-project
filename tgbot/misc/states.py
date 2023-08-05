from aiogram.dispatcher.filters.state import StatesGroup, State


class UsersStates(StatesGroup):
    """
    Класс реализует состояние пользователя внутри сценария.
    Атрибуты заполняются во время опроса пользователя. Очищаются при каждой новой команде.

    Attributes:
        last_command (str): команда, которую ввёл пользователь.
        user_id (int): id Telegram.
        user_username (str): username в Telegram.
        user_fullname (str): ФИО в Telegram.
        user_phone (str): номер телефона.
        user_message (str): сообщение пользователя.
        current_page (int): текущая страница пагинации.
    """

    last_command = State()
    user_id = State()
    user_username = State()
    user_fullname = State()
    user_phone = State()
    user_message = State()
    current_page = State()
