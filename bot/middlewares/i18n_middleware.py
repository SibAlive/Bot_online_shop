import logging
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import User

from bot.services import UserService


logger = logging.getLogger(__name__)


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user: User = data.get("event_from_user")
        session = data.get("session")
        user_service = UserService(session)

        if user is None:
            return await handler(event, data)

        state: FSMContext = data.get("state")
        user_context_data = await state.get_data()

        if (user_lang := user_context_data.get("user_lang")) is None:
            if session is None:
                logger.error("Database connection not found in middleware data.")
                raise RuntimeError("Missing database connection for detecting the user's language")

            user_lang: str | None = await user_service.get_user_lang(user_id=user.id)
            if user_lang is None:
                user_lang = user.language_code

        translations: dict = data.get("translations")
        i18n: dict = translations.get(user_lang)

        if i18n is None:
            data['i18n'] = translations[translations["default"]]
        else:
            data['i18n'] = i18n

        return await handler(event, data)