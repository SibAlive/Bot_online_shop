import logging
from aiogram import BaseMiddleware
from aiogram.types import User

from bot.services import UserService


logger = logging.getLogger(__name__)


class ShadowBanMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        logger.debug(
            f"Вошли в миддлварь {__class__.__name__}, тип события {event.__class__.__name__}",
        )
        user: User = data.get("event_from_user")
        session = data.get("session")
        user_service = UserService(session)

        if user is None:
            return await handler(event, data)

        if session is None:
            logger.error("Database connection bot found in middleware data.")
            raise RuntimeError("Missing database connection for shadow ban check.")

        user_banned_status = await user_service.get_user_banned_status_by_id(user_id=user.id)

        if user_banned_status:
            logger.warning(f"Shadow-banned user tried to interact: {user.id}")
            if event.callback_query:
                await event.callback_query.answer()
            return

        result = await handler(event, data)
        logger.debug(f"Выходим из миддлвари  {__class__.__name__}")
        return result