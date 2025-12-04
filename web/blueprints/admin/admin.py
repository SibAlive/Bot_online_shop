"""Маршруты для управления категориями и товарами"""
from flask import redirect, url_for, render_template, flash, request, Blueprint
from flask_httpauth import HTTPBasicAuth
from functools import wraps

from web.extensions import db
from web.forms import CategoryForm, ProductForm
from web.url_creator import ADMIN_USERNAME, ADMIN_PASSWORD
from web.services import build_product_sort_column
from bot.models import Category, Product


admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static'
)

"""Устанавливаем вход в админ панель по логину и паролю"""
# Добавляем Basic Auth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return username
    return None

@auth.error_handler
def unauthorized():
    return "Доступ запрещен", 401

# Оборачиваем все маршруты админки в декоратор auth.login_required
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return auth.login_required(f)(*args, **kwargs)
    return decorated_function


@admin.before_request
@auth.login_required
def require_admin_auth():
    pass

"""--- Главная страница ---"""
@admin.route('/')
def index():
    return redirect(url_for('.categories'))


"""--- Категории ---"""
@admin.route('/categories', methods=['GET'])
def categories():
    """Отображает все категории"""
    categories_list = Category.query.all()
    return render_template('categories.html', categories=categories_list)


@admin.route('/category/new', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        # Проверка уникальности наименования
        if Category.query.filter_by(name=form.name.data).first():
            flash('Категория с таким именем уже существует!', 'danger')
            return render_template(
                'category_form.html',
                form=form,
                title="Новая категория"
            )

        category = Category(
            name=form.name.data,
            is_active=form.is_active.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Категория создана!', 'success')
        return redirect(url_for('.categories'))

    return render_template(
        'category_form.html',
        form=form,
        title="Новая категория"
    )

@admin.route('/category/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        # Проверка уникальности наименования (кроме текущего)
        existing = Category.query.filter(
            Category.name == form.name.data,
            Category.id != id
        ).first()
        if existing:
            flash('Наименование уже используется другой категорией!', 'danger')
            return render_template(
                'category_form.html',
                form=form,
                title="Редактировать категорию"
            )

        category.name = form.name.data
        category.is_active = form.is_active.data
        db.session.commit()
        flash('Категория обновлена!', 'success')
        return redirect(url_for('.categories'))

    return render_template(
        'category_form.html',
        form=form,
        title="Редактировать категорию"
    )

@admin.route('/category/delete/<int:id>', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    # Проверяем, есть ли товары в этой категории
    if category.products:
        flash('Нельзя удалить категорию - в ней есть товары!', 'danger')
        return redirect(url_for('.categories'))

    db.session.delete(category)
    db.session.commit()
    flash('Категория удалена!', 'success')
    return redirect(url_for('.categories'))


"""--- Товары ---"""
@admin.route('/products', methods=['GET'])
def products():
    """Добавляем сортировку товаров по категориям"""
    # Получаем ID категории из GET-параметра
    category_id = request.args.get('category_id', type=int)

    # Запрос товаров: фильтруем по категории, если category_id передан
    query = Product.query
    if category_id:
        query = query.filter(Product.category_id == category_id)

    # Сортируем
    sort_column, sort_by, order = build_product_sort_column('product_name')

    products_list = query.order_by(sort_column).all()

    # Получаем все активные категории дл фильтра
    categories_list = Category.query.filter_by(is_active=True).all()

    return render_template(
        'products.html',
        products=products_list,
        categories=categories_list,
        selected_category_id=category_id,
        sort_by=sort_by,
        order=order
    )

@admin.route('/product/new', methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        photo_url = form.photo_url.data

        category_id = form.category_id.data if form.category_id.data != 0 else None

        product = Product(
            name=form.name.data,
            price=form.price.data,
            photo_url=photo_url,
            category_id=category_id,
            is_available=form.is_available.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Товар добавлен!', 'success')
        return redirect(url_for('.products'))

    return render_template('product_form.html', form=form, title="Новый товар")


@admin.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        photo_url = form.photo_url.data

        category_id = form.category_id.data if form.category_id.data != 0 else None

        product.name = form.name.data
        product.price = form.price.data
        product.photo_url = photo_url
        product.category_id = category_id
        product.is_available = form.is_available.data

        db.session.commit()
        flash('Товар обновлён!', 'success')
        return redirect(url_for('.products'))

    # Предзаполним текущие значения
    form.category_id.data = product.category_id or 0
    return render_template('product_form.html', form=form, title="Редактировать товар")


@admin.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Товар удалён!', 'success')
    return redirect(url_for('.products'))