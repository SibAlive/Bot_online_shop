import logging
from aiogram import Router, F, Bot
from aiogram.enums import BotCommandScopeType
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (Message, CallbackQuery, InputMediaPhoto,
                           ChatMemberUpdated, BotCommandScopeChat)
from aiogram.filters import CommandStart, Command, StateFilter, ChatMemberUpdatedFilter, KICKED
from sqlalchemy.ext.asyncio import AsyncSession

from services import (ProductService, UserService, CartService, index_increase,
                      index_decrease, create_text_order, convert_total,
                      get_confirm_text, get_caption, get_keyboard_bottom_text)
from keyboards import (create_keyboard_categories, create_keyboard_bottom,
                       create_keyboard_confirm, create_keyboard_cart,
                       create_main_keyboard, create_main_menu_commands)
from filters import (IsDelItemCallbackData, IsCorrectNameMessage, IsCorrectNumberMessage,
                     ButtonCartFilter, ButtonContactsFilter, ButtonOrderFilter,
                     ButtonCategoryFilter)
from FSM import OrderForm


logger = logging.getLogger(__name__)

# Инициализируем роутер модуля
user_router = Router()


# Этот хэндлер будет срабатывать на команду /start
@user_router.message(CommandStart())
async def process_start_command(
        message: Message,
        bot: Bot,
        session: AsyncSession,
        i18n: dict
):
    logger.debug("Вошли в хэндлер, обрабатывающий команду /start")
    user_service = UserService(session)
    user_role = await user_service.get_user_role(user_id=message.from_user.id)

    await message.answer(
        text=i18n.get('/start_registered'),
        reply_markup=create_main_keyboard(i18n),
    )

    commands = create_main_menu_commands(i18n, role=user_role)
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT,
            chat_id=message.from_user.id
        )
    )
    logger.debug("Выходим из хэндлера, обрабатывающего команду /start")


# Этот хэндлер будет срабатывать на команду /cancel в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@user_router.message(Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message, i18n: dict):
    await message.answer(text=i18n.get("cancel_command"))


# Этот хэндлер будет срабатывать на команду /cancel в любых состояниях,
# кроме состояния по умолчанию и отключать машину состояний
@user_router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message:Message, state: FSMContext, i18n: dict):
    sent = await message.answer(text=i18n.get("cancel_command_success"))

    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.update_data(name=None, phone=None, address=None, message_ids=[sent.message_id])
    await state.set_state()

# Этот хэндлер будет срабатывать при нажатии кнопки корзина
@user_router.message(ButtonCartFilter(), StateFilter(default_state))
async def process_button_cart(
        message: Message,
        session: AsyncSession,
        i18n: dict,
        state: FSMContext
):
    logger.debug("Входим в хэндлер корзины")
    user_id = message.from_user.id
    cart_service = CartService(session)
    total = await cart_service.get_cart_total(user_id=user_id)
    products_in_cart = await cart_service.get_cart_items_with_info(user_id=user_id)
    if total:
        text = convert_total(total, i18n)
        sent = await message.answer(
            text=text,
            reply_markup=await create_keyboard_cart(i18n=i18n, products=products_in_cart)
        )
    else:
        sent = await message.answer(text=i18n.get("cart_empty"))

    await state.update_data(message_ids=[sent.message_id])
    logger.debug("Выходим из хэндлера корзины")


# Этот хэндлер будет срабатывать на нажатие инлайн кнопки удалить
@user_router.callback_query(IsDelItemCallbackData(), StateFilter(default_state))
async def process_del_press(
        callback: CallbackQuery,
        i18n: dict,
        session: AsyncSession,
        state: FSMContext,
        product_id_to_delete: int
):
    logger.debug("Входим в хэндлер срабатывающий на нажатие инлайн кнопки удалить")
    user_id = callback.from_user.id
    cart_service = CartService(session)
    await cart_service.remove_from_cart(
        user_id=callback.from_user.id,
        product_id=product_id_to_delete
    )
    total = await cart_service.get_cart_total(user_id=user_id)
    products_in_cart = await cart_service.get_cart_items_with_info(user_id=user_id)
    if total:
        text = convert_total(total, i18n)
        sent = await callback.message.edit_text(
            text=text,
            reply_markup=await create_keyboard_cart(i18n=i18n, products=products_in_cart)
        )
    else:
        sent = await callback.message.edit_text(text=i18n.get("cart_empty"))

    await state.update_data(message_ids=[sent.message_id])
    logger.debug("Выходим из хэндлера срабатывающего на нажатие инлайн кнопки удалить")


# Этот хэндлер будет срабатывать при нажатии кнопки категории
@user_router.message(ButtonCategoryFilter(), StateFilter(default_state))
async def process_button_category(
        message: Message,
        session: AsyncSession,
        i18n: dict,
        state: FSMContext
):
    logger.debug(f"Входим в хэндлер кнопки категории")
    product_service = ProductService(session)
    categories = await product_service.get_all_categories()

    if not categories:
        await message.answer(i18n.get("categories_not_found"))
        return

    sent = await message.answer(
        text=i18n.get('category'),
        reply_markup = create_keyboard_categories(categories)
    )
    await state.update_data(message_ids=[sent.message_id])
    logger.debug("Выходим из хэндлера кнопки категории")


# Этот хэндлер будет срабатывать на нажатие кнопки оформить заказ
@user_router.message(ButtonOrderFilter(), StateFilter(default_state))
async def process_button_order(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        i18n: dict
):
    logger.debug("Входим в хэндлер оформить заказ")
    cart_service = CartService(session)
    products_in_cart = await cart_service.get_cart_items_with_info(user_id=message.from_user.id)
    result = await create_text_order(i18n=i18n, products=products_in_cart)

    if type(result) is not tuple:
        sent = await message.answer(text=result)
        await state.update_data(message_ids=[sent.message_id])
    else:
        sent_1 = await message.answer(text=result[0])
        sent_2 = await message.answer(text=result[1])
        sent_3 = await message.answer(text=f"{result[2]}\n{i18n.get("cancel_write")}")
        await state.update_data(message_ids=[sent_1.message_id, sent_2.message_id, sent_3.message_id])
        await state.set_state(OrderForm.fill_name) # Устанавливаем состояние ожидания ввода имени

    logger.debug("Выходим из хэндлера оформить заказ")

# Этот хэндлер будет срабатывать на нажатие кнопки контакты
@user_router.message(ButtonContactsFilter(), StateFilter(default_state))
async def process_button_contacts(message: Message, i18n: dict, state: FSMContext):
    logger.debug("Входим в хэндлер контакты")
    sent = await message.answer(text=i18n.get('contacts'))
    await state.update_data(message_ids=[sent.message_id])
    logger.debug(f"Выходим из хэндлера контакты")

# Этот хэндлер будет срабатывать на нажатие любой из категории
@user_router.callback_query(F.data.startswith("category_"), StateFilter(default_state))
async def process_products_choice(
        callback: CallbackQuery,
        session:AsyncSession,
        i18n: dict,
        state: FSMContext):
    logger.debug("Входим в хэндлер нажатие любой из категории")
    category_id = int(callback.data.split("_")[1])

    product_service = ProductService(session)
    # Получаем список товаров из выбранной категории
    products = await product_service.get_products_by_category(category_id)
    if not products:
        await callback.answer(i18n.get("items_not_found"), show_alert=True)

    # Показываем первый товар
    product = products[0]
    caption = get_caption(product)

    await state.update_data(
        index=0,
        current_product_id=product.id,
        category_id=category_id,
    )

    # Формируем количество товаров в корзине (нижняя кнопка)
    text = await get_keyboard_bottom_text(product.id, i18n, session, user_id=callback.from_user.id)
    sent = await callback.message.edit_media(
        media=InputMediaPhoto(
            media=product.photo_url,
            caption=caption,
        ),
        reply_markup=await create_keyboard_bottom(i18n=i18n, text=text)
    )

    await state.update_data(message_ids=[sent.message_id])
    logger.debug("Выходим из хэндлера нажатие любой из категории")

# Этот хэндлер будет срабатывать на нажатие кнопок next и prev
@user_router.callback_query(F.data.in_(('next', 'prev')), StateFilter(default_state))
async def process_next_inline_press(
        callback: CallbackQuery,
        session: AsyncSession,
        i18n: dict,
        state: FSMContext
):
    logger.debug("Входим в хэндлер next или prev")
    product_service = ProductService(session)

    if callback.data == 'prev':
        category_id, index = await index_decrease(state, session)
    elif callback.data == 'next':
        category_id, index = await index_increase(state, session)

    # Список продуктов из выбранной категории
    products = await product_service.get_products_by_category(category_id)
    # Показываем текущий товар
    product = products[index]
    caption = get_caption(product)
    text = await get_keyboard_bottom_text(product.id, i18n, session, user_id=callback.from_user.id)

    try:
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=product.photo_url,
                caption=caption,
            ),
            reply_markup=await create_keyboard_bottom(i18n=i18n, text=text)
        )
    except TelegramBadRequest:
        await callback.answer()
    logger.debug("Выходим из хэндлера next или prev")


# Этот хэндлер будет срабатывать при нажатии кнопки добавить в корзину
@user_router.callback_query(F.data == "add_to_cart", StateFilter(default_state))
async def process_add_to_cart(
        callback: CallbackQuery,
        session: AsyncSession,
        i18n: dict,
        state: FSMContext
):
    logger.debug("Входим в хэндлер добавить в корзину")
    data = await state.get_data()
    product_id = data.get('current_product_id')
    product_service = ProductService(session)
    cart_service = CartService(session)

    # Получаем товар из БД
    product = await product_service.get_product_by_id(product_id)
    # Добавляем товар в корзину
    await cart_service.add_to_cart(
        user_id=callback.from_user.id,
        product_id=product_id
    )
    caption = get_caption(product)
    text = await get_keyboard_bottom_text(product.id, i18n, session, user_id=callback.from_user.id)

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=product.photo_url,
            caption=caption,
        ),
        reply_markup=await create_keyboard_bottom(i18n=i18n, text=text)
    )

    await callback.answer(i18n.get("item_added"))
    logger.debug("Выходим из хэндлера добавить в корзину")


# Хэндлер для ввода имени
@user_router.message(OrderForm.fill_name, IsCorrectNameMessage())
async def process_name(message: Message, state: FSMContext, name, i18n: dict):
    await state.update_data(name=name)  # Временно сохраняем данные внутри контекста
    sent = await message.answer(text=f"{i18n.get("write_phone")}\n{i18n.get("cancel_write")}")
    await state.set_state(OrderForm.fill_phone)   # Устанавливаем состояние ожидания ввода телефона
    await state.update_data(message_ids=[sent.message_id])


# Хэндлер для ввода имени (некорректное значение)
@user_router.message(OrderForm.fill_name)
async def process_incorrect_name(message:Message, i18n: dict, state: FSMContext):
    sent = await message.answer(text=f"{i18n.get('write_correct_name')}\n{i18n.get("cancel_write")}")
    await state.update_data(message_ids=[sent.message_id])


# Хэндлер для ввода телефона
@user_router.message(OrderForm.fill_phone, IsCorrectNumberMessage())
async def process_phone(message: Message, state: FSMContext, phone, i18n: dict):
    await state.update_data(phone=phone)    # Временно сохраняем данные внутри контекста
    sent = await message.answer(i18n.get("write_address"))
    await state.set_state(OrderForm.fill_address) # Устанавливаем состояние ожидания ввода адреса
    await state.update_data(message_ids=[sent.message_id])


# Хэндлер для ввода телефона (некорректное значение)
@user_router.message(OrderForm.fill_phone)
async def process_incorrect_phone(message: Message, i18n: dict, state: FSMContext):
    sent = await message.answer(text=f"{i18n.get('write_correct_phone')}\n{i18n.get("cancel_write")}")
    await state.update_data(message_ids=[sent.message_id])


# Хэндлер для ввода адреса
@user_router.message(OrderForm.fill_address, F.text)
async def process_address(message: Message, state: FSMContext, i18n: dict):
    address = message.text.strip()
    await state.update_data(address=address)    # Временно сохраняем данные внутри контекста

    data = await state.get_data()   # Получаем данные из временного хранилища в виде словаря
    answer = get_confirm_text(data, i18n) # функция, возвращающая строку для ответа

    sent = await message.answer(text=answer, reply_markup=create_keyboard_confirm(i18n))
    await state.set_state(OrderForm.fill_correct) # Устанавливаем состояние ожидания подтверждения
    await state.update_data(message_ids=[sent.message_id])


# Этот хэндлер будет срабатывать при нажатии на инлайн кнопку correct
@user_router.callback_query(OrderForm.fill_correct, F.data == "correct")
async def process_correct(callback: CallbackQuery, state: FSMContext, i18n: dict):
    # Удаляем предыдущее сообщение
    data = await state.get_data()
    message_id = data.get('message_ids')[0]
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=message_id
    )

    sent = await callback.message.answer(text=i18n.get('write_name'))
    await state.set_state(OrderForm.fill_name)  # Запускаем ожидание ввода имени
    await state.update_data(message_ids=[sent.message_id])


# Этот хэндлер будет срабатывать при нажатии на инлайн кнопку confirm
@user_router.callback_query(OrderForm.fill_correct, F.data == "confirm")
async def process_confirm(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
        i18n: dict
):
    # Удаляем предыдущее сообщение
    data = await state.get_data()
    message_id = data.get('message_ids')[0]
    await callback.bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=message_id
    )


    await callback.message.answer(text=i18n.get('thanks_for_order'))

    # Очищаем корзину
    cart_service = CartService(session)
    await cart_service.clear_cart(user_id=callback.from_user.id)

    # Сбрасываем форму заполнения данных
    await state.update_data(name=None, phone=None, address=None)
    await state.set_state()


# Этот хэндлер будет срабаывать на любые сообщения в состоянии ожидания подтверждения
@user_router.message(OrderForm.fill_correct)
async def process_unknown_command(message: Message, state: FSMContext, i18n: dict):
    logger.debug("Входим в хэндлер срабатывающий на любые сообщения в состоянии ожидания подтверждения")
    data = await state.get_data()  # Получаем данные из временного хранилища в виде словаря
    answer = get_confirm_text(data, i18n)  # функция, возвращающая строку для ответа

    sent = await message.answer(text=answer, reply_markup=create_keyboard_confirm(i18n))
    await state.update_data(message_ids=[sent.message_id])
    logger.debug("Выходим из хэндлера срабатывающего на любые сообщения в состоянии ожидания подтверждения")


# Блокировка бота пользователем
@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    logger.info(f"User {event.from_user.id} has blocked the bot")
    user_service = UserService(session)
    await user_service.change_user_alive_status(is_alive=False, user_id=event.from_user.id)