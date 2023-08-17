from aiogram.dispatcher.filters.state import StatesGroup, State


class UsersStates(StatesGroup):
    """
    Класс реализует состояние пользователя внутри сценария.
    Атрибуты заполняются во время опроса пользователя. Очищаются при каждой новой команде.

    Attributes:
        last_command (str): команда, которую ввёл пользователь.
        user_id (int): id пользователя вTelegram.
        user_fullname (str): ФИО в Telegram.
        user_phone (str): номер телефона.
        current_page (int): текущая страница пагинации.
        user (TGUser): пользователь
    """

    last_command = State()
    user_id = State()
    user_fullname = State()
    user_phone = State()


class ProductStates(StatesGroup):
    categories = State()
    product_id = State()
