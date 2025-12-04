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


# Форма массовой рассылки
class BroadcastForm(StatesGroup):
    choose = State() # Ожидаем выбор типа сообщения
    message = State() # Ожидаем сообщение/описание
    file = State() # Ожидаем фото, видео или документ
    caption = State() # Ожидаем описание (опционально)
    confirm = State()  # Ожидаем подтверждения отправки