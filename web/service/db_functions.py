import logging
from sqlalchemy import select

from bot.models import Category, Product


logger = logging.getLogger(__name__)

# Проверка
class CategoryService:
    def __init__(self, db):
        self.db = db

    def get_categories_list(self):
        """Возвращает список всех категорий"""
        try:
            categories = self.db.session.execute(
                select(Category)
                .order_by(Category.id)
            ).scalars().all()

            if not categories:
                logger.warning("Категории отсутствуют")
            return categories
        except Exception as e:
            logger.error("Ошибка получения данных из БД" + str(e))

    def get_active_categories(self):
        """Возвращает список активных категорий"""
        active_categories = self.db.session.execute(
            select(Category)
            .where(Category.is_active == True)
        ).scalars().all()
        return active_categories

    def get_category_by_id(self, *, id):
        """Возвращает категорию по ее id"""
        category = self.db.session.execute(
            select(Category)
            .where(Category.id == id)
        ).scalar_one_or_none()
        return category

    def create_category(self, *, form):
        """Создает новую категорию, проверяя уникальность наименования"""
        # Проверка уникальности наименования категории
        category_check = self.db.session.execute(
            select(Category)
            .where(Category.name == form.name.data)
        ).first()
        if category_check:
            return False

        # Создаем новую категорию
        category = Category(
            name=form.name.data,
            is_active=form.is_active.data
        )
        self.db.session.add(category)
        self.db.session.commit()
        return True

    def edit_category(self, *, form, category, id):
        """Редактирует существующую категорию, проверяя уникальность наименования"""
        # Проверка уникальности наименования
        exiting = self.db.session.execute(
            select(Category)
            .where(Category.name == form.name.data, Category.id != id)
        ).scalar_one_or_none()
        if exiting:
            return False

        # Редактирование категории
        category.name = form.name.data
        category.is_active = form.is_active.data
        self.db.session.commit()
        return True

    def delete_category(self, *, id):
        """Удаляет выбранную категорию, проверяя наличие в ней товаров"""
        category = self.get_category_by_id(id=id)
        if category.products:
            return False

        self.db.session.delete(category)
        self.db.session.commit()
        return True


class ProductService:
    def __init__(self, db):
        self.db = db

    def get_products_list(self, *, category_id, sort_column):
        """Возвращает список товаров с сортировкой по категориям"""
        # Запрос товаров: фильтруем по категории, если category_id передан
        stmt = select(Product)
        if category_id:
            stmt = stmt.where(Product.category_id == category_id)

        # Сортируем
        stmt = stmt.order_by(sort_column)

        products = self.db.session.execute(stmt).scalars().all()
        return products

    def get_product_by_id(self, id):
        product = self.db.session.execute(
            select(Product)
            .where(Product.id == id)
        ).scalar_one_or_none()
        return product

    def create_product(self, *, form):
        """Создает новый товар"""
        category_id = form.category_id.data if form.category_id.data != 0 else None

        product = Product(
            name=form.name.data,
            price=form.price.data,
            photo_url=form.photo_url.data,
            category_id=category_id,
            is_available=form.is_available.data
        )
        self.db.session.add(product)
        self.db.session.commit()

    def edit_product(self, *, form, product):
        """Редактирует существующий товар, проверяя уникальность наименования"""
        category_id = form.category_id.data if form.category_id.data != 0 else None

        product.name = form.name.data
        product.price = form.price.data
        product.photo_url = form.photo_url.data
        product.category_id = category_id
        product.is_available = form.is_available.data

        self.db.session.commit()

    def delete_product(self, *, id):
        product = self.get_product_by_id(id=id)
        self.db.session.delete(product)
        self.db.session.commit()