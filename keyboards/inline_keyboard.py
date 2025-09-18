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
            [InlineKeyboardButton(text=text, callback_data='add_to_cart')]
        ]
    )
    return inline_keyboard_bottom


# Функция, генерирующая инлайн кнопки для корзины
async def create_keyboard_cart(i18n: dict, products: list[dict]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for product in products:
        kb_builder.row(
            InlineKeyboardButton(
                text=f"{product.get('name')} - {product.get('qnty')} {i18n.get("edit_cart_button")}",
                callback_data=f"{product.get('id')}_del"
            )
        )
    return kb_builder.as_markup()


def create_keyboard_confirm(i18n: dict):
    # инлайн кнопки подтверждения данных
    buttons = [
        [InlineKeyboardButton(text=i18n.get('correct'), callback_data='correct'),
         InlineKeyboardButton(text=i18n.get('confirm'), callback_data='confirm')
         ]
    ]
    inline_keyboard_confirm = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard_confirm