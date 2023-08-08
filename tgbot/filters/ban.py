import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.models.commands import get_banned_ids


class BanFilter(BoundFilter):
    key = 'is_banned'

    def __init__(self, is_banned: typing.Optional[bool] = None):
        self.is_banned = is_banned

    async def check(self, obj):
        if self.is_banned is None:
            return False
        banned_ids = await get_banned_ids()
        return (obj.from_user.id in banned_ids) == self.is_banned
