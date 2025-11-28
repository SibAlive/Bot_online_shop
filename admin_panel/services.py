from flask import request

from models import User, CartItem, Category, Product


def build_product_sort_column(s_by):
    """Функция для построения базового запроса записей"""
    # по умолчанию сортируем по времени
    sort_by = request.args.get('sort_by', s_by)
    if sort_by == 'time':
        order = request.args.get('order', 'desc')
    else:
        order = request.args.get('order', 'asc')

    sort_columns = {
        'product_name': Product.name,
        'price': Product.price,
    }
    sort_column = sort_columns.get(sort_by)

    sort_column = sort_column.desc().nulls_last() if order == 'desc' else sort_column.asc().nulls_first()
    return sort_column, sort_by, order