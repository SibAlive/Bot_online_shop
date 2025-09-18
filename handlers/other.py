import logging
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message


logger = logging.getLogger(__name__)

other_router = Router()


# Срабатывает на отправку фото
@other_router.message(F.photo, StateFilter(default_state))
async def process_photo_message(message: Message, state: FSMContext, i18n: dict):
    sent = await message.answer(text=i18n.get('need_admin_rights'))
    await state.update_data(message_ids=[sent.message_id])


# Этот хэндлер будет срабатывать на все текстовые сообщения
@other_router.message(StateFilter(default_state))
async def process_any_message(message: Message, i18n: dict, state: FSMContext):
    logger.debug(f"Входим в хэндлер любое сообщение")
    sent = await message.answer(text=i18n.get("Unknown command"))
    await state.update_data(message_ids=[sent.message_id])
    logger.debug(f"Выходим из хэндлера любое сообщение")