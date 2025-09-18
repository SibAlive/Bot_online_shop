import logging
import time
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from redis.asyncio import Redis


logger = logging.getLogger(__name__)


""" Middleware для защиты от спама"""
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, limit: int, tm: int):
        self.redis = redis
        self.limit = limit    # лимит сообщений в единицу времени
        self.tm = tm  # время

    async def __call__(self, handler, event, data):
        logger.debug(
            f"Вошли в миддлварь {__class__.__name__}, тип события {event.__class__.__name__}",
        )
        i18n = data.get("i18n")
        state: FSMContext = data.get("state")

        if not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        key = f"rate_limit:{user_id}"
        current = int(time.time())

        # Считает количество запросов в текущем окне
        count = await self.redis.zcount(key, current - self.tm, current)
        if count >= self.limit:
            # Отправляем сообщение пользователю
            sent = await event.answer(i18n.get("dont_flood"))
            # Не перезаписываем message_ids, а добавляем id сообщений в список
            # на случай, если пользователь будет отправлять много сообщений подряд
            user_context_data = await state.get_data()
            message_ids = user_context_data.get("message_ids", [])
            message_ids.append(sent.message_id)
            await state.update_data(message_ids=message_ids)
            return

        # Добавляем текущий timestamp
        await self.redis.zadd(key, {current: current})
        # Устанавливаем TTL для автоматического удаления
        await self.redis.expire(key, self.tm + 10)

        return await handler(event, data)