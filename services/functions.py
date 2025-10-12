import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from services import ProductService, Product, CartService, CartItem


logger = logging.getLogger(__name__)


# Функция увеличивает индекс пользователя
async def index_increase(state: FSMContext, session: AsyncSession) -> tuple[int, int]:
    product_service = ProductService(session)
    data = await state.get_data()
    index = data.get("index")
    category_id = data.get("category_id")

    if index < len(await product_service.get_products_by_category(category_id=category_id)) - 1:
        index += 1
    else:
        index = 0

    products = await product_service.get_products_by_category(category_id=data['category_id'])
    if products:
        current_product = products[index]
        data.update(
            index=index,
            current_product_id=current_product.id
        )
    # Сохраняем изменения
    await state.set_data(data)

    return category_id, index


# Функция уменьшает индекс пользователя
async def index_decrease(state: FSMContext, session: AsyncSession) -> tuple[int, int]:
    product_service = ProductService(session)
    data = await state.get_data()
    index = data.get("index")
    category_id = data.get("category_id")

    if index == 0:
        index = len(await product_service.get_products_by_category(category_id=category_id)) - 1
    else:
        index -= 1

    products = await product_service.get_products_by_category(category_id=data['category_id'])
    if products:
        current_product: Product = products[index]
        data.update(
            index=index,
            current_product_id=current_product.id
        )
    # Сохраняем изменения
    await state.set_data(data)

    return category_id, index


# Функция формирует текст содержимого корзины
def create_cart_goods(products: list[dict], i18n: dict):
    text = '\n'.join(f"{product.get('name')} - {product.get('qnty')};" for product in products)
    return text


# Функция конвертирует общую сумму корзины
def convert_total(total: int, i18n: dict) -> str:
    # total = '\n'.join(f"{product.get('name')} - {product.get('qnty')};" for product in products)
    total = '\n' + '\n' + i18n.get("calculate_cart").format(total).replace(',', ' ')
    return total


# Функция формирует текст сообщения, при нажатии на кнопку оформить заказ
async def create_text_order(i18n: dict, products: list[dict]) -> tuple | str:
    text = ""
    total = 0

    for product in products:
        name = product.get('name')
        qnty = product.get('qnty')
        price = product.get('price')
        total += price * qnty
        text += (f"{name}: {qnty} * {price:,.2f} сум = {total:,.2f} сум;\n"
                   .replace(',', ' '))

    if text:
        result_1 = i18n.get("your_order_total").format(total).replace(',', ' ')
        result_2 = text
        return result_1, result_2

    text = i18n.get("order_cart_empty")
    return text


def get_confirm_text(data: dict, i18n: dict) -> tuple:
    """Формирует текст подтверждения ввода данных"""
    name = data.get("name")
    phone = data.get("phone")
    address = data.get("address")
    result = i18n.get("confirm_text").format(name, phone, address)

    check_str, *details = result.split('\n')
    details = '\n'.join(details)

    return check_str, details


def get_confirm_text_from_db(user_details: list[dict], i18n: dict) -> tuple:
    name = user_details[0].get("name")
    phone = user_details[0].get("phone")
    address = user_details[0].get("address")
    result = i18n.get("confirm_text").format(name, phone, address)

    check_str, *details = result.split('\n')
    details = '\n'.join(details)

    return check_str, details


def get_thanks_for_order_text(user_details: list[dict], i18n: dict) -> str:
    """Формирует текст подтверждения заказа"""
    name = user_details[0].get("name")
    phone = user_details[0].get("phone")
    address = user_details[0].get("address")
    result = i18n.get("thanks_for_order").format(name, phone, address)
    return result


def get_caption(product: Product) -> str:
    price = f"{product.price:,}".replace(',', ' ')
    caption = f"<i>{product.name}</i>\nЦена: <b>{price} сум</b>"
    return caption


async def get_keyboard_bottom_text(
        current_product_id: int,
        i18n: dict,
        session: AsyncSession,
        user_id: int
) -> str:

    cart_service = CartService(session)
    cart: list[CartItem] = await cart_service.get_cart_items(user_id)

    result = i18n.get('add_to_cart')
    qnty = 0
    for item in cart:
        if current_product_id == item.product_id:
            qnty = item.quantity
    result += f" ({qnty})"
    return result


async def delete_prev_messages(bot: Bot, data: dict, chat_id: int) -> None:
    message_ids = data.get('message_ids', [])
    for message_id in message_ids:
        try:
            await bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
        except TelegramBadRequest:
            pass


def convert_list_users_to_str(lst_users: list[tuple]) -> str:
    """Конвертирует список пользователей в строку"""
    result = ""
    for user in lst_users:
        result += f"ID: {user[0]} - {user[1]}\n"
    return result