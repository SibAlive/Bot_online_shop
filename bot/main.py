"""Запуск бота через Polling, используется для отладки"""
import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import Config, load_config
from bot.services import AsyncSessionLocal, engine
from bot.lexicon.i18n import get_translations
from bot.handlers import router
from bot.middlewares import (DataBaseMiddleware, ShadowBanMiddleware, UserRegistrationMiddleware,
                             DeleteLastMessageMiddleware, TranslatorMiddleware, LangSettingsMiddleware,
                             ThrottlingMiddleware)


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
    logger.info("Проверка автодеплоя")

    # Инициализируем хранилище
    redis = Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password or None,
            username=config.redis.username or None,
        )
    storage = RedisStorage(redis)

    try:
        # Отправляем команду PING
        pong = await redis.ping()
        logger.info(f"Connection successful! PONG: {pong}")
    except Exception as e:
        logger.info(f"Connection to Redis failed: {e}")

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)
    # dp = Dispatcher()

    # Получаем словарь с переводами
    translations = get_translations()

    # Регистрируем роутеры в диспетчере
    logger.info("Including routers...")
    dp.include_router(router)

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
        await bot.session.close()
        # await redis.aclose()
        logger.info("Connection to PostgresSQL closed")


# Политика цикла событий для Windows
if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass


"""Запуск бота через Webhook на удаленном сервере, финальная версия"""
# import sys
# import os
# import asyncio
# import logging
# from functools import partial
# from aiogram import Bot, Dispatcher
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.fsm.storage.redis import RedisStorage
# from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
# from aiohttp import web
# from redis.asyncio import Redis
# from sqlalchemy import text
#
# from config import Config, load_config
# from bot.services import AsyncSessionLocal, engine
# from bot.lexicon.i18n import get_translations
# from bot.handlers import router
# from bot.middlewares import (DataBaseMiddleware, ShadowBanMiddleware, UserRegistrationMiddleware,
#                          DeleteLastMessageMiddleware, TranslatorMiddleware, LangSettingsMiddleware,
#                          ThrottlingMiddleware)
#
#
# # Инициализируем логгер
# logger = logging.getLogger(__name__)
#
#
# async def on_startup(bot: Bot, config: Config, redis: Redis) -> None:
#     """Устанавливаем webhook при запуске"""
#     webhook_url = config.webhook.base_url + config.webhook.path
#     webhook_secret = config.webhook.secret
#     logger.info(f"Attempting to set webhook to: {webhook_url}")
#
#     # Проверка подключения к Redis
#     try:
#         await redis.ping()
#         logger.info("Successfully connected to Redis")
#     except Exception as e:
#         logger.error(f"Failed to connect to Redis: {e}")
#         raise e
#
#     # Проверка PostgreSQL
#     try:
#         async with engine.begin() as conn:
#             await conn.execute(text("SELECT 1"))
#         logger.info("Successfully connected to PostgreSQL")
#     except Exception as e:
#         logger.error(f"Failed to connect to PostgreSQL: {e}")
#         raise e
#
#     # Устанавливаем webhook в Telegram
#     try:
#         await bot.set_webhook(
#             url=webhook_url,
#             secret_token=webhook_secret,
#             drop_pending_updates=False,  # Очистка старых обновлений при запуске
#         )
#         logger.info(f"Webhook set to: {webhook_url}")
#     except Exception as e:
#         logger.exception("Failed to set webhook")
#         raise e
#
#
# async def on_shutdown(bot: Bot) -> None:
#     """Удаляем вебхук только если не на Render"""
#     if not os.getenv("RENDER"):
#         await bot.delete_webhook(drop_pending_updates=True)
#         logger.info("Webhook deleted")
#     else:
#         logger.info("Skipping webhook deletion on Render")
#
#     # Закрываем соединения
#     await bot.session.close()
#     if hasattr(bot, "_redis"):
#         await bot._redis.close()
#         logger.info("Redis closed")
#     await engine.dispose()
#     logger.info("Connection to Redis and PostgreSQL closed")
#
#
# # Функция конфигурирования и запуск бота
# def create_app() -> web.Application:
#     # Загружаем конфиг в переменную конфиг
#     config: Config = load_config()
#
#     # Задаем базовую конфигурацию логирования
#     logging.basicConfig(
#         level=logging.getLevelName(level=config.log.level),
#         format=config.log.format
#     )
#     # Выводи в консоль информацию о начале запуска бота
#     logger.info("Starting bot...")
#
#     # Инициализируем хранилище
#     redis = Redis(
#         host=config.redis.host,
#         port=config.redis.port,
#         db=config.redis.db,
#         password=config.redis.password,
#         username=config.redis.username,
#     )
#     storage = RedisStorage(redis)
#
#     # Инициализируем бот и диспетчер
#     bot = Bot(
#         token=config.bot.token,
#         default=DefaultBotProperties(parse_mode=ParseMode.HTML),
#     )
#     dp = Dispatcher(storage=storage)
#
#     # Получаем словарь с переводами
#     translations = get_translations()
#
#     # Регистрируем роутеры в диспетчере
#     logger.info("Including routers...")
#     dp.include_router(router)
#
#     # Регистрируем миддлвари
#     logger.info("Including middlewares...")
#     dp.update.middleware(DataBaseMiddleware())
#     dp.update.middleware(ShadowBanMiddleware())
#     dp.update.middleware(LangSettingsMiddleware())
#     dp.update.middleware(TranslatorMiddleware())
#     dp.message.middleware(UserRegistrationMiddleware())
#     dp.message.middleware(DeleteLastMessageMiddleware())
#     dp.message.middleware(ThrottlingMiddleware(redis, limit=1, tm=1))
#
#     # Регистрируем события жизненного цикла
#     dp.startup.register(partial(on_startup, bot, config, redis))
#     dp.shutdown.register(on_shutdown)
#
#     # Создаем объект aiohttp приложения
#     app = web.Application()
#
#     # Создаем обработчик запросов от Telegram
#     try:
#         webhook_handler = SimpleRequestHandler(
#             dispatcher=dp,
#             bot=bot,
#             translations=translations,
#             session=AsyncSessionLocal,
#             admin_ids=config.bot.admin_ids,
#         )
#     except Exception as e:
#         logger.exception(f"Failed to dispatch webhook: {e}")
#         raise e
#     webhook_handler.register(app, path=config.webhook.path)
#
#     # Подключаем диспетчер к приложению (для graceful shutdown и т.п.)
#     setup_application(app, dp, bot=bot)
#
#     # Health check endpoint для Render
#     async def health_check(request):
#         return web.Response(text="OK", status=200)
#     app.router.add_get("/", health_check)
#     app.router.add_get("/health", health_check)
#
#     logger.info("Application created successfully")
#     return app
#
#
# # Политика цикла событий для Windows
# if sys.platform.startswith("win") or os.name == "nt":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#
# app = create_app()
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8000))
#     web.run_app(app, host="0.0.0.0", port=port)