from aiogram.fsm.state import StatesGroup, State


# Форма выбора языка
class LangForm(StatesGroup):
    lang = State()

# Форма заполнения данных для заказа
class OrderForm(StatesGroup):
    fill_name = State() # Ожидаем имя
    fill_phone = State() # Ожидаем телефон
    fill_address = State() # Ожидаем адрес
    fill_correct = State() # Ожидаем подтверждение