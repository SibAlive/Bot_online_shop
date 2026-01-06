"""Маршруты для управления категориями и товарами"""
from flask import redirect, url_for, render_template, flash, request, Blueprint
from flask_httpauth import HTTPBasicAuth
from functools import wraps

from web.extensions import db
from web.forms import CategoryForm, ProductForm
from web.url_creator import ADMIN_USERNAME, ADMIN_PASSWORD
from web.service import build_product_sort_column, CategoryService, ProductService


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
    category_service = CategoryService(db)
    categories_list = category_service.get_categories_list()
    return render_template('categories.html', categories=categories_list)


@admin.route('/category/new', methods=['GET', 'POST'])
def new_category():
    category_service = CategoryService(db)
    form = CategoryForm()
    if form.validate_on_submit():
        # Проверяем уникальности наименования и создаем новую категорию
        if not category_service.create_category(form=form):
            flash('Категория с таким именем уже существует!', 'danger')
            return render_template(
                'category_form.html',
                form=form,
                title="Новая категория"
            )

        flash('Категория создана!', 'success')
        return redirect(url_for('.categories'))

    return render_template(
        'category_form.html',
        form=form,
        title="Новая категория"
    )

@admin.route('/category/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category_service = CategoryService(db)
    category = category_service.get_category_by_id(id=id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        # Проверка уникальности наименования (кроме текущего)
        if not category_service.edit_category(form=form, category=category, id=id):
            flash('Наименование уже используется другой категорией!', 'danger')
            return render_template(
                'category_form.html',
                form=form,
                title="Редактировать категорию"
            )

        flash('Категория обновлена!', 'success')
        return redirect(url_for('.categories'))

    return render_template(
        'category_form.html',
        form=form,
        title="Редактировать категорию"
    )

@admin.route('/category/delete/<int:id>', methods=['POST'])
def delete_category(id):
    category_service = CategoryService(db)
    # Проверяем, есть ли товары в этой категории
    if not category_service.delete_category(id=id):
        flash('Нельзя удалить категорию - в ней есть товары!', 'danger')
        return redirect(url_for('.categories'))

    flash('Категория удалена!', 'success')
    return redirect(url_for('.categories'))


"""--- Товары ---"""
@admin.route('/products', methods=['GET'])
def products():
    """Возвращает список товаров с сортировкой по категориям"""
    # Получаем ID категории из GET-параметра
    category_id = request.args.get('category_id', type=int)
    product_service = ProductService(db)
    category_service = CategoryService(db)

    # Получаем значения для сортировки
    sort_column, sort_by, order = build_product_sort_column('product_name')
    # Получаем список продуктов
    products_list = product_service.get_products_list(category_id=category_id, sort_column=sort_column)

    # Получаем все активные категории для фильтра
    categories_list = category_service.get_active_categories()

    return render_template(
        'products.html',
        products=products_list,
        categories=categories_list,
        selected_category_id=category_id,
        sort_by=sort_by,
        order=order,
    )

@admin.route('/product/new', methods=['GET', 'POST'])
def new_product():
    product_service = ProductService(db)
    form = ProductForm()
    if form.validate_on_submit():
        product_service.create_product(form=form)
        flash('Товар добавлен!', 'success')
        return redirect(url_for('.products'))
    return render_template('product_form.html', form=form, title="Новый товар")


@admin.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product_service = ProductService(db)
    product = product_service.get_product_by_id(id=id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product_service.edit_product(form=form, product=product)
        flash('Товар обновлён!', 'success')
        return redirect(url_for('.products'))

    # Предзаполним текущие значения
    form.category_id.data = product.category_id or 0
    return render_template('product_form.html', form=form, title="Редактировать товар")


@admin.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product_service = ProductService(db)
    product_service.delete_product(id=id)
    flash('Товар удалён!', 'success')
    return redirect(url_for('.products'))