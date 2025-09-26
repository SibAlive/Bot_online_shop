from flask import Flask
import os

from .extensions import db
from .routers import (index, categories, new_category,edit_category,
                     delete_category, products, new_product, edit_product,
                     delete_product)
from services import DATABASE_URL_FOR_FLASK


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL_FOR_FLASK
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 МБ максимальный размер файла

    # Создаем папку для загрузок, если ее нет
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Инициализируем расширения
    db.init_app(app)

    # Регистрируем маршруты
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/categories', 'categories', categories, methods=['GET'])
    app.add_url_rule('/category/new', 'new_category', new_category, methods=['GET', 'POST'])
    app.add_url_rule('/category/edit/<int:id>', 'edit_category', edit_category, methods=['GET', 'POST'])
    app.add_url_rule('/category/delete/<int:id>', 'delete_category', delete_category, methods=['POST'])

    app.add_url_rule('/products', 'products', products, methods=['GET'])
    app.add_url_rule('/product/new', 'new_product', new_product, methods=['GET', 'POST'])
    app.add_url_rule('/product/edit/<int:id>', 'edit_product', edit_product, methods=['GET', 'POST'])
    app.add_url_rule('/product/delete/<int:id>', 'delete_product', delete_product, methods=['POST'])

    return app