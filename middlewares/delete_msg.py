import logging
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest


logger = logging.getLogger(__name__)


class DeleteLastMessageMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        logger.debug(
            f"Вошли в миддлварь {__class__.__name__,}, тип события {event.__class__.__name__,}",
            )

        state: FSMContext = data.get("state")
        user_context_data = await state.get_data()
        message_ids = user_context_data.get("message_ids", [])

        # Удаляем все предыдущие сообщения
        for message_id in message_ids:
            if message_id:
                try:
                    await data['bot'].delete_message(
                        chat_id=event.chat.id,
                        message_id=message_id
                    )
                    logger.debug("Сообщение удалено")
                except TelegramBadRequest:
                    pass

        logger.debug(f"Выходим из миддлвари  {__class__.__name__}")
        return await handler(event, data)