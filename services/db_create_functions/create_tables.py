import asyncio
import logging
import os
import sys

from config.config import Config, load_config
from online_shop.models.models import Base
from services.connections import engine

# Загрузка конфига
config: Config = load_config()

# Настройка логирования
logging.basicConfig(
    level=logging.getLevelName(level=config.log.level),
    format=config.log.format,
)
logger = logging.getLogger(__name__)

# Политика цикла событий для Windows
if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def create_tables(engine):
    """Создает таблицы, если их нет"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблицы успешно созданы")


async def main():
    try:
        # Создаем таблицы
        await create_tables(engine)
    except Exception as e:
        logger.exception(f"Ошибка при создании таблиц: {e}")
    finally:
        # Закрываем движок
        await engine.dispose()
        logger.info("Соединение с PostgreSQL закрыто")


if __name__ == "__main__":
    asyncio.run(main())