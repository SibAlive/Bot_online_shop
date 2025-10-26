from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, BotCommand

from enums import UserRole


def create_main_keyboard(i18n):
    # Создаем объекты кнопок
    button_cart = KeyboardButton(text=i18n.get("button_cart"))
    button_category = KeyboardButton(text=i18n.get("button_category"))
    button_contacts = KeyboardButton(text=i18n.get("button_contacts"))

    # Создаем объект клавиатуры
    main_keyboard = ReplyKeyboardMarkup(keyboard=[
        [button_cart, button_category],
        [button_contacts]
    ],
    resize_keyboard=True,)

    return main_keyboard


def create_main_menu_commands(i18n: dict, role: UserRole):
    if role in (UserRole.USER, UserRole.MODERATOR):
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
                command="/users",
                description=i18n.get("/users_description")
            ),
            BotCommand(
                command='/ban',
                description=i18n.get('/ban_description')
            ),
            BotCommand(
                command='/unban',
                description=i18n.get('/unban_description')
            ),
            BotCommand(
                command='/moder',
                description=i18n.get('/moder_description')
            ),
            BotCommand(
                command='/unmoder',
                description=i18n.get('/unmoder_description')
            ),
            BotCommand(
                command='/broadcast',
                description=i18n.get('/broadcast_description')
            )
        ]


def create_phone_keyboard():
    phone_button = KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[[phone_button]],
        resize_keyboard=True,
        one_time_keyboard=True # Клавиатура исчезнет после нажатия
    )
    return phone_keyboard