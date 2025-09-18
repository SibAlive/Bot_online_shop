import logging
from contextlib import suppress

from aiogram import Bot, F, Router
from aiogram.enums import BotCommandScopeType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter, CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, BotCommandScopeChat
from sqlalchemy.ext.asyncio import AsyncSession

from FSM import LangForm
from keyboards import create_main_keyboard, create_main_menu_commands, get_lang_settings_kb
from services import UserService
from filters import LocaleFilter


logger = logging.getLogger(__name__)

settings_router = Router()


# Срабатывает на любое сообщение, кроме команды /start, в состоянии 'LangFrom.lang'
@settings_router.message(StateFilter(LangForm.lang), ~CommandStart())
async def process_any_message_when_lang(
        message: Message,
        bot: Bot,
        i18n: dict[str, str],
        translations: dict[str, str],
        state: FSMContext
):
    user_id = message.from_user.id
    locales = list(translations.keys())
    data = await state.get_data()
    user_lang = data.get("user_lang")

    with suppress(TelegramBadRequest):
        msg_id = data.get("message_ids")[0]
        if msg_id:
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=msg_id)

    sent = await message.answer(
        text=i18n.get("choose_lang"),
        reply_markup=get_lang_settings_kb(i18n=i18n, locales=locales, checked=user_lang)
    )
    await state.update_data(message_ids=[sent.message_id])


# Срабатывает на команду /lang
@settings_router.message(Command(commands='lang'))
async def process_lang_command(
        message: Message,
        i18n: dict[str, str],
        session: AsyncSession,
        translations: dict[str, str],
        state: FSMContext,
):
    locales = list(translations.keys())
    user_service = UserService(session)
    await state.set_state(LangForm.lang)
    user_lang = await user_service.get_user_lang(user_id=message.from_user.id)

    sent = await message.answer(
        text=i18n.get("choose_lang"),
        reply_markup=get_lang_settings_kb(i18n=i18n, locales=locales, checked=user_lang)
    )
    await state.update_data(user_lang=user_lang, message_ids=[sent.message_id])


# Нажатие кнопки "Сохранить" в режиме настроек языка
@settings_router.callback_query(F.data == "save_lang_button_data")
async def process_save_click(
        callback: CallbackQuery,
        bot: Bot,
        i18n: dict,
        session: AsyncSession,
        state: FSMContext
):
    user_service = UserService(session)
    user_role = await user_service.get_user_role(user_id=callback.from_user.id)
    data = await state.get_data()

    await user_service.update_user_lang(
        language=data.get('user_lang') ,
        user_id=callback.from_user.id
    )

    # Удаляем предыдущее сообщение
    message_id = data.get('message_ids')[0]
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=message_id
    )

    await callback.message.answer(
        text=i18n.get("lang_saved"),
        reply_markup=create_main_keyboard(i18n)
    )

    commands = create_main_menu_commands(i18n, role=user_role)
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT,
            chat_id=callback.from_user.id
        )
    )

    await state.update_data(user_lang=None)
    await state.set_state()


# Нажатие кнопки "Отмена" в режиме настроек языка
@settings_router.callback_query(F.data == "cancel_lang_button_data")
async def process_cancel_click(
        callback: CallbackQuery,
        state: FSMContext,
        i18n: dict[str, str],
        session: AsyncSession,
):
    user_service = UserService(session)
    user_lang = await user_service.get_user_lang(user_id=callback.from_user.id)
    await callback.message.edit_text(text=i18n.get("lang_cancelled").format(i18n.get(user_lang)))
    await state.update_data(user_lang=None)
    await state.set_state()


# Нажатие любой радио-кнопки с локалью в режиме настроек языка интерфейса
@settings_router.callback_query(LocaleFilter())
async def process_lang_click(
        callback: CallbackQuery, i18n: dict[str, str], translations: dict[str, str]
):
    locales = list(translations.keys())
    try:
        await callback.message.edit_text(
            text=i18n.get("choose_lang"),
            reply_markup=get_lang_settings_kb(i18n=i18n, locales=locales, checked=callback.data)
        )
    except TelegramBadRequest:
        await callback.answer()