import logging
from aiogram import Router, F
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from enums import UserRole
from filters import UserRoleFilter
from services import UserService, convert_list_users_to_str

loger = logging.getLogger(__name__)

admin_router = Router()

# Подключаем фильтр UserRoleFilter ко всем хэндлерам роутера
admin_router.message.filter(UserRoleFilter(UserRole.ADMIN))


# Команда /users
@admin_router.message(Command('users'))
async def process_users_command(message, session):
    """Выводит список пользователей"""
    user_service = UserService(session)
    users_lst = await user_service.get_users_list()
    text = convert_list_users_to_str(users_lst)
    await message.answer(text=text)


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
        await message.reply(i18n.get('empty_ban_answer'))
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


@admin_router.message(Command('moder'))
async def process_moder_command(message, command, session, i18n):
    """Наделяет пользователя правами модератора"""
    # Сохраняем в переменную args текст, который следует после '/ban'
    args = command.args
    # Создаем экземпляр класса с функциями управления пользователями
    user_service = UserService(session)

    if not args:
        await message.reply(i18n.get('empty_moder_answer'))
        return

    # Убираем лишний текст и пробелы, если имеются
    arg_user = args.split()[0].strip()

    if arg_user.isdigit():
        user_status = await user_service.get_user_role(user_id=int(arg_user))
    else:
        await message.reply(text=i18n.get('incorrect_moder_arg'))
        return

    if not user_status:
        await message.reply(i18n.get('no_user'))
    elif user_status == UserRole.ADMIN:
        await message.reply(i18n.get('it_is_admin'))
    elif user_status == UserRole.MODERATOR:
        await message.reply(i18n.get('already_moder'))
    else:
        await user_service.change_user_role(user_id=int(arg_user), role=UserRole.MODERATOR)
        await message.reply(text=i18n.get('successfully_moder'))


@admin_router.message(Command('unmoder'))
async def process_moder_command(message, command, session, i18n):
    """Удаляет у пользователя права модератора"""
    # Сохраняем в переменную args текст, который следует после '/ban'
    args = command.args
    # Создаем экземпляр класса с функциями управления пользователями
    user_service = UserService(session)

    if not args:
        await message.reply(i18n.get('empty_moder_answer'))
        return

    # Убираем лишний текст и пробелы, если имеются
    arg_user = args.split()[0].strip()

    if arg_user.isdigit():
        user_status = await user_service.get_user_role(user_id=int(arg_user))
    else:
        await message.reply(text=i18n.get('incorrect_moder_arg'))
        return

    if not user_status:
        await message.reply(i18n.get('no_user'))
    elif user_status == UserRole.ADMIN:
        await message.reply(i18n.get('it_is_admin'))
    elif user_status == UserRole.USER:
        await message.reply(i18n.get('already_user'))
    else:
        await user_service.change_user_role(user_id=int(arg_user), role=UserRole.USER)
        await message.reply(text=i18n.get('successfully_unmoder'))


# Срабатывает на отправку фото (возвращает в чат file_id)
# file_id необходим для добавления фото в базу данных
@admin_router.message(F.photo, StateFilter(default_state))
async def process_any_message(message: Message, state: FSMContext):
    sent = await message.reply(text=f"file_id = \n<code>{message.photo[-1].file_id}</code>")