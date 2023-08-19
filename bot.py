import asyncio
import django
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.ban import BanFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.ban import register_ban
from tgbot.handlers.call import register_call
from tgbot.handlers.echo import register_echo
from tgbot.handlers.help import register_help
from tgbot.handlers.menu import register_menu
from tgbot.handlers.mess import register_mess
from tgbot.handlers.start import register_start
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.services.default_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(BanFilter)


def register_all_handlers(dp):
    register_ban(dp)
    register_admin(dp)
    register_start(dp)
    register_call(dp)
    register_mess(dp)
    register_menu(dp)
    register_help(dp)

    register_echo(dp)


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "dj_ac.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    setup_django()
    config = load_config(".env")

    storage = RedisStorage2(config.redis.host, config.redis.port, db=5, pool_size=10, prefix='bot_fsm') \
        if config.redis.use_redis else MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)
    await set_default_commands(bot)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
