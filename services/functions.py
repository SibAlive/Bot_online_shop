import logging
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


# Функция конвертирует общую сумму корзины
def convert_total(total: int, i18n: dict) -> str:
    return i18n.get("calculate_cart").format(total).replace(',', ' ')


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
        result_3 = i18n.get('write_name')
        return result_1, result_2, result_3

    text = i18n.get("order_cart_empty")
    return text


# Функция, формирующая текст подтверждения ввода данных
def get_confirm_text(data: dict[str, str], i18n: dict) -> str:
    name = data.get('name')
    phone = data.get('phone')
    address = data.get('address')

    result = i18n.get("confirm_text").format(name, phone, address)

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