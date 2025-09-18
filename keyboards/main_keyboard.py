from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, BotCommand

from enums import UserRole


def create_main_keyboard(i18n):
    # Создаем объекты кнопок
    button_cart = KeyboardButton(text=i18n.get("button_cart"))
    button_category = KeyboardButton(text=i18n.get("button_category"))
    button_order = KeyboardButton(text=i18n.get("button_order"))
    button_contacts = KeyboardButton(text=i18n.get("button_contacts"))

    # Создаем объект клавиатуры
    main_keyboard = ReplyKeyboardMarkup(keyboard=[
        [button_cart, button_category],
        [button_order],
        [button_contacts]
    ],
    resize_keyboard=True,)

    return main_keyboard


def create_main_menu_commands(i18n: dict, role: UserRole):

    if role == UserRole.USER:
        return [
            BotCommand(
                command="/start",
                description=i18n.get("/start_description"),
            ),
            BotCommand(
                command="/lang",
                description=i18n.get("/lang_description")
            )
        ]
    elif role == UserRole.ADMIN:
        return [
            BotCommand(
                command="/start",
                description=i18n.get("/start_description"),
            ),
            BotCommand(
                command="/lang",
                description=i18n.get("/lang_description")
            ),
            BotCommand(
                command='/ban',
                description=i18n.get('/ban_description')
            ),
            BotCommand(
                command='/unban',
                description=i18n.get('/unban_description')
            )
        ]