import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config.config import Config, load_config
from services.connections import AsyncSessionLocal, engine
from handlers.settings import settings_router
from handlers.admin import admin_router
from handlers.user import user_router
from handlers.other import other_router
from middlewares.database_middleware import DataBaseMiddleware
from middlewares.shadow_ban import ShadowBanMiddleware
from middlewares.check_reg import UserRegistrationMiddleware
from middlewares.delete_msg import DeleteLastMessageMiddleware
from middlewares.i18n_middleware import TranslatorMiddleware
from middlewares.lang_settings import LangSettingsMiddleware
from middlewares.throttling_middleware import ThrottlingMiddleware
from lexicon.i18n import get_translations


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуск бота
async def main() -> None:
    # Загружаем конфиг в переменную конфиг
    config: Config = load_config()

    # Задаем базовую конфигурацию логирования
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format
    )
    # Выводи в консоль информацию о начале запуска бота
    logger.info("Starting bot...")

    # Инициализируем хранилище
    redis = Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
            username=config.redis.username,
        )
    storage = RedisStorage(redis)

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Получаем словарь с переводами
    translations = get_translations()

    # Регистрируем роутеры в диспетчере
    logger.info("Including routers...")
    dp.include_routers(settings_router, admin_router, user_router, other_router)

    # Регистрируем миддлвари
    logger.info("Including middlewares...")
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(ShadowBanMiddleware())
    dp.update.middleware(LangSettingsMiddleware())
    dp.update.middleware(TranslatorMiddleware())
    dp.message.middleware(UserRegistrationMiddleware())
    dp.message.middleware(DeleteLastMessageMiddleware())
    dp.message.middleware(ThrottlingMiddleware(redis, limit=1, tm=1))

    # Запускаем polling
    try:
        await dp.start_polling(
                        bot,
                        translations=translations,
                        session=AsyncSessionLocal,
                        admin_ids=config.bot.admin_ids,
        )
    except Exception as e:
        logger.exception(e)
    finally:
        # Закрываем движок
        await engine.dispose()
        logger.info("Connection to PostgresSQL closed")


# Политика цикла событий для Windows
if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    asyncio.run(main())