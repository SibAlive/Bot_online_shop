"""table online_shop_users renamed to users

Revision ID: d298933644d6
Revises: 3209a1d5cc58
Create Date: 2025-09-28 16:14:28.166434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd298933644d6'
down_revision: Union[str, Sequence[str], None] = '3209a1d5cc58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Переименовываем таблицу
    op.rename_table('online_shop_users', 'users')


def downgrade() -> None:
    """Downgrade schema."""
    # Возвращаем старое имя при откате
    op.rename_table('users', 'online_shop_users')
