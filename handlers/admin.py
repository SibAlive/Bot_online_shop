import logging
from aiogram import Router, F
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from enums import UserRole
from filters import UserRoleFilter
from services import UserService


loger = logging.getLogger(__name__)

admin_router = Router()

# Подключаем фильтр UserRoleFilter ко всем хэндлерам роутера
admin_router.message.filter(UserRoleFilter(UserRole.ADMIN))


# Команда /ban
@admin_router.message(Command('ban'))
async def process_ban_command(message: Message, command: CommandObject,
                              session: AsyncSession, i18n: dict) -> None:
    # Сохраняем в переменную args текст, который следует после '/ban'
    args = command.args
    # Создаем экземпляр класса с функциями управления пользователями
    user_service = UserService(session)

    if not args:
        await message.reply(i18n.get('empty_ban_answer'))
        return

    # Убираем лишний текст и пробелы, если имеются
    arg_user = args.split()[0].strip()

    if arg_user.isdigit():
        banned_status = await user_service.get_user_banned_status_by_id(user_id=int(arg_user))
    elif arg_user.startswith('@'):
        banned_status = await user_service.get_user_banned_status_by_username(username=arg_user[1:])
    else:
        await message.reply(text=i18n.get('incorrect_ban_arg'))
        return

    if banned_status is None:
        await message.reply(i18n.get('no_user'))
    elif banned_status:
        await message.reply(i18n.get('already_banned'))
    else:
        if arg_user.isdigit():
            await user_service.change_user_banned_status_by_id(user_id=int(arg_user), banned=True)
        else:
            await user_service.change_user_banned_status_by_username(username=arg_user[1:], banned=True)
        await message.reply(text=i18n.get('successfully_banned'))


# Команда /unban
@admin_router.message(Command('unban'))
async def process_unban_command(message: Message, command: CommandObject,
                                session: AsyncSession, i18n: dict[str, str]) -> None:
    # Сохраняем в переменную args текст, который следует после '/unban'
    args = command.args
    # Создаем экземпляр класса с функциями управления пользователями
    user_service = UserService(session)

    if not args:
        await message.reply(i18n.get('empty_unban_answer'))
        return

    arg_user = args.split()[0].strip()

    if arg_user.isdigit():
        banned_status = await user_service.get_user_banned_status_by_id(user_id=int(arg_user))
    elif arg_user.startswith('@'):
        banned_status = await user_service.get_user_banned_status_by_username(username=arg_user[1:])
    else:
        await message.reply(text=i18n.get('incorrect_unban_arg'))
        return

    if banned_status is None:
        await message.reply(i18n.get('no_user'))
    elif banned_status:
        if arg_user.isdigit():
            await user_service.change_user_banned_status_by_id(user_id=int(arg_user), banned=False)
        else:
            await user_service.change_user_banned_status_by_username(username=arg_user[1:], banned=False)
        await message.reply(text=i18n.get('successfully_unbanned'))
    else:
        await message.reply(text=i18n.get('not_banned'))


# Срабатывает на отправку фото (возвращает в чат file_id)
# file_id необходим для добавления фото в базу данных
@admin_router.message(F.photo, StateFilter(default_state))
async def process_any_message(message: Message, state: FSMContext):
    sent = await message.answer(text=f"file_id = \n<code>{message.photo[-1].file_id}</code>")
    await state.update_data(message_ids=[sent.message_id])