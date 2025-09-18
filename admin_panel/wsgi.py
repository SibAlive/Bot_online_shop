"""Данный модуль необходим для запуска админ панели через терминал"""
# Чтобы запустить админ панель через терминал, необходимо ввести:
# waitress-serve --host=0.0.0.0 --port=5000 "online_shop.admin_panel.wsgi:application"

from app import create_app


# Создаем приложение
application = create_app()