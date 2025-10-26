from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Инлайн кнопки с выбором языка
def get_lang_settings_kb(i18n: dict, locales: list[str], checked: str) -> InlineKeyboardMarkup:
    buttons = []
    for locale in sorted(locales):
        if locale == "default":
            continue
        if locale == checked:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"🔘 {i18n.get(locale)}", callback_data=locale
                    )
                ]
            )
        else:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"⚪️ {i18n.get(locale)}", callback_data=locale
                    )
                ]
            )

    buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("cancel_lang_button_text"),
                callback_data="cancel_lang_button_data"
            ),
            InlineKeyboardButton(
                text=i18n.get("save_lang_button_text"),
                callback_data="save_lang_button_data"
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# инлайн кнопки с категориями товаров
def create_keyboard_categories(categories: list):
    buttons = [InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}")
               for category in categories]
    keyboard_lst = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    inline_keyboard_category = InlineKeyboardMarkup(inline_keyboard=keyboard_lst)
    return inline_keyboard_category


# функция, генерирующая инлайн кнопки для товаров
async def create_keyboard_bottom(i18n: dict, text: str):
    inline_keyboard_bottom = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.get('prev'), callback_data='prev'),
             InlineKeyboardButton(text=i18n.get('next'), callback_data='next')],
            [InlineKeyboardButton(text=text, callback_data='add_to_cart')],
            [InlineKeyboardButton(text=i18n.get('back'), callback_data='back_to_categories')],
        ]
    )
    return inline_keyboard_bottom


async def create_keyboard_cart(i18n: dict) -> InlineKeyboardMarkup:
    """# Функция, генерирующая инлайн кнопки корзины"""
    inline_keyboard_cart = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=i18n.get('edit_order'), callback_data='edit_order'),
            InlineKeyboardButton(text=i18n.get('place_an_order'), callback_data='place_an_order')],
        ]
    )
    return inline_keyboard_cart


async def create_keyboard_edit_cart(i18n: dict, products: list[dict]) -> InlineKeyboardMarkup:
    """Функция генерирует инлайн клавиатуру редактирования корзины"""
    kb_builder = InlineKeyboardBuilder()
    for product in products:
        kb_builder.row(
            InlineKeyboardButton(
                text=f"{product.get('name')} - {product.get('qnty')} {i18n.get("edit_cart_button")}",
                callback_data=f"{product.get('id')}_del"
            )
        )

    # Добавляем в конец кнопку назад
    kb_builder.row(
        InlineKeyboardButton(text=i18n.get('back'), callback_data='back_to_cart')
    )

    return kb_builder.as_markup()


def create_keyboard_confirm(i18n: dict):
    # инлайн кнопки подтверждения данных
    buttons = [
        [InlineKeyboardButton(text=i18n.get('correct'), callback_data='correct'),
         InlineKeyboardButton(text=i18n.get('confirm'), callback_data='confirm')
         ],
        [InlineKeyboardButton(text=i18n.get('back'), callback_data='back_from_confirm')]
    ]
    inline_keyboard_confirm = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard_confirm


def create_keyboard_broadcast():
    buttons = [
        [InlineKeyboardButton(text='Сообщение', callback_data='message'),
         InlineKeyboardButton(text='Фото', callback_data='photo')
         ],
        [InlineKeyboardButton(text='Видео', callback_data='video'),
         InlineKeyboardButton(text='Документ', callback_data='document')
         ],
        [InlineKeyboardButton(text='Отмена', callback_data='cancel_broadcast')]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


def create_keyboard_affirm_broadcast():
    buttons = [
        [InlineKeyboardButton(text='Разослать', callback_data='broadcast_send')],
        [InlineKeyboardButton(text='Отмена', callback_data='broadcast_send_cancel')]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


def create_keyboard_broadcast_caption():
    buttons = [
        [InlineKeyboardButton(text='Без описания', callback_data='no_caption'),
         ]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


def create_keyboard_back_to_broadcast():
    buttons = [
        [InlineKeyboardButton(text='Назад', callback_data='back_to_broadcast'),
         ]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard