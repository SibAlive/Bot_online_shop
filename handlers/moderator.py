import logging
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from enums import UserRole
from filters import UserRoleFilter


logger = logging.getLogger(__name__)

moderator_router = Router()


# Срабатывает на отправку фото (возвращает в чат file_id)
# file_id необходим для добавления фото в базу данных
@moderator_router.message(F.photo, UserRoleFilter(UserRole.MODERATOR), StateFilter(default_state))
async def process_any_message(message: Message, state: FSMContext):
    sent = await message.reply(text=f"file_id = \n<code>{message.photo[-1].file_id}</code>")