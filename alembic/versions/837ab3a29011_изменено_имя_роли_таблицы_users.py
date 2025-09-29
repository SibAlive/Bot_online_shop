"""Изменено имя роли таблицы users

Revision ID: 837ab3a29011
Revises: d298933644d6
Create Date: 2025-09-29 22:34:18.546048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '837ab3a29011'
down_revision: Union[str, Sequence[str], None] = 'd298933644d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Определяем ENUM один раз для переиспользования
user_role_enum = postgresql.ENUM('USER', 'ADMIN', name='user_role_enum', create_type=False)

def upgrade() -> None:
    # 1. Создаём НОВЫЙ ENUM-тип
    new_enum = postgresql.ENUM('USER', 'ADMIN', name='user_role_enum')
    new_enum.create(op.get_bind(), checkfirst=True)

    # 2. Преобразуем колонку: сначала приводим к TEXT, потом к новому ENUM
    op.alter_column(
        'users', 'role',
        existing_type=postgresql.ENUM('USER', 'ADMIN', name='user_rolw_enum'),
        type_=sa.Text(),  # временно в текст
        existing_nullable=False
    )
    op.alter_column(
        'users', 'role',
        existing_type=sa.Text(),
        type_=new_enum,
        existing_nullable=False,
        postgresql_using="role::text::user_role_enum"  # явное приведение
    )

    # 3. Удаляем СТАРЫЙ ENUM (если он больше не нужен)
    old_enum = postgresql.ENUM('USER', 'ADMIN', name='user_rolw_enum')
    old_enum.drop(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    # Восстанавливаем старый ENUM
    old_enum = postgresql.ENUM('USER', 'ADMIN', name='user_rolw_enum')
    old_enum.create(op.get_bind(), checkfirst=True)

    # Обратное преобразование
    op.alter_column(
        'users', 'role',
        existing_type=postgresql.ENUM('USER', 'ADMIN', name='user_role_enum'),
        type_=sa.Text(),
        existing_nullable=False
    )
    op.alter_column(
        'users', 'role',
        existing_type=sa.Text(),
        type_=old_enum,
        existing_nullable=False,
        postgresql_using="role::text::user_rolw_enum"
    )

    # Удаляем новый ENUM
    new_enum = postgresql.ENUM('USER', 'ADMIN', name='user_role_enum')
    new_enum.drop(op.get_bind(), checkfirst=True)