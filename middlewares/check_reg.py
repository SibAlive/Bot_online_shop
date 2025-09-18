import logging
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import create_main_keyboard
from services import UserService
from enums import UserRole


logger = logging.getLogger(__name__)


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        logger.debug(
            f"Вошли в миддлварь {__class__.__name__}, тип события {event.__class__.__name__}",
        )
        user = event.from_user

        session: AsyncSession = data.get("session")
        user_service = UserService(session)
        i18n = data.get("i18n")
        admin_ids = data.get("admin_ids")

        if not session:
            logger.error("Сессия БД не передана в UserRegistrationMiddleware")
            return await handler(event, data)

        # Проверяем есть ли пользователь в БД
        user_row = await user_service.get_user(user_id=user.id)
        if user_row is None:
            # Устанавливаем роль нового пользователя
            user_role = UserRole.ADMIN if user.id in admin_ids else UserRole.USER

            # Регистрируем нового пользователя
            await user_service.add_user(
                user_id=user.id,
                username=user.username,
                language=user.language_code or 'ru',
                role=user_role,
            )

            await event.bot.send_message(
                chat_id=user.id,
                text=i18n.get("wellcome").format(user.first_name),
                reply_markup=create_main_keyboard(i18n)
            )

        else:
            # Если пользователь уже зарегистрирован, меняем его 'is_alive' статус на True,
            # На случай, если пользователь ранее блокировал бота
            await user_service.change_user_alive_status(
                is_alive=True,
                user_id=user.id,
            )

        result = await handler(event, data)
        logger.debug(f"Выходим из миддлвари  {__class__.__name__}")
        return result