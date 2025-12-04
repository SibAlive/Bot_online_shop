import logging
from typing import Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_

from bot.enums import UserRole
from bot.models import User, Category, Product, CartItem

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(
            self,
            *,
            user_id: int,
            username: str | None = None,
            language: str = 'ru',
            role: UserRole = UserRole.USER,
            is_alive: bool = True,
            banned: bool = False,
    ) -> None:
        """Добавляет пользователя в базу данных"""
        new_user = User(
            user_id=user_id,
            username=username,
            language=language,
            role=role,
            is_alive=is_alive,
            banned=banned,
        )
        self.session.add(new_user)
        await self.session.commit()

        logger.info(
            f"User added. Table='users', user_id={user_id}, "
            f"created_at={datetime.now(timezone.utc)}, language={language}, "
            f"role={role}, is_alive={is_alive}, banned={banned}"
        )

    async def get_user(self, *, user_id: int) -> tuple[Any, ...] | None:
        """Возвращает кортеж данных пользователя"""
        result = await self.session.execute(
            select(
                User.id,
                User.user_id,
                User.username,
                User.language,
                User.role,
                User.is_alive,
                User.banned,
                User.created_at,
            ).where(User.user_id == user_id)
        )
        row = result.fetchone()
        logger.info(f"Row is {row}")
        return row if row else None

    async def get_users_list(self):
        """Возвращает список пользователей"""
        result = await self.session.execute(
            select(User.user_id, User.username)
        )
        row = result.fetchall()
        return row

    async def get_user_lang(self, *, user_id: int) -> str | None:
        """Возвращает язык пользователя"""
        result = await self.session.execute(
            select(User.language).where(User.user_id == user_id)
        )
        row = result.fetchone()
        if row:
            logger.info(f"The user with {user_id} has the language {row[0]}")
            return row[0]
        else:
            logger.warning(f"No user with 'user_id' {user_id} found in the database")
            return None

    async def update_user_lang(
            self,
            *,
            language: str,
            user_id: int,
    ) -> None:
        """Обновляет язык пользователя"""
        await self.session.execute(
            update(User).where(User.user_id == user_id).values(language=language)
        )
        await self.session.commit()
        logger.info(f"The language {language} is set for the user {user_id}")

    async def change_user_alive_status(
            self,
            *,
            is_alive: bool,
            user_id: int,
    ) -> None:
        """Изменяет 'alive' статус пользователя"""
        await self.session.execute(
            update(User).where(User.user_id == user_id).values(is_alive=is_alive)
        )
        await self.session.commit()
        logger.info(f"Updated 'is_alive' status to {is_alive} for user {user_id}")

    async def get_user_role(self, *, user_id: int, ) -> UserRole | None:
        """Возвращает роль пользователя"""
        result = await self.session.execute(
            select(User.role).where(User.user_id == user_id)
        )
        row = result.fetchone()
        if row:
            logger.info(f"The user with 'user_id'={user_id} has the role is {row[0]}")
            return UserRole(row[0])  # Конвертируем в Enum
        else:
            logger.warning(f"No user with 'user_id'={user_id} found in the database")
            return None

    async def change_user_role(self, *, user_id: int, role: UserRole) -> None:
        """Меняет роль пользователя"""
        await self.session.execute(
            update(User).where(User.user_id == user_id).values(role=role)
        )
        await self.session.commit()

    async def get_user_alive_status(self, *, user_id: int, ) -> bool | None:
        """Возвращает 'alive' статус пользователя"""
        result = await self.session.execute(
            select(User.is_alive).where(User.user_id == user_id)
        )
        row = result.fetchone()
        if row:
            logger.info(f"The user with 'user_id'={user_id} has the is_alive status is {row[0]}")
            return row[0]
        else:
            logger.warning(f"No user with 'user_id'={user_id} found in the database")
            return None

    async def get_user_banned_status_by_id(self, *, user_id: int, ) -> bool | None:
        """Возвращает статус бана пользователя по его id"""
        result = await self.session.execute(
            select(User.banned).where(User.user_id == user_id)
        )
        row = result.fetchone()
        if row:
            logger.info(f"The user with 'user_id'={user_id} has the banned status is {row[0]}")
            return row[0]
        else:
            logger.warning(f"No users with 'user_id={user_id} found in the database")
            return None

    async def get_user_banned_status_by_username(self, *, username: str, ) -> bool | None:
        """Возвращает статус бана пользователя по его username"""
        result = await self.session.execute(
            select(User.banned).where(User.username == username)
        )
        row = result.fetchone()
        if row:
            logger.info(f"The user with 'username'={username} has the banned status is {row[0]}")
            return row[0]
        else:
            logger.warning(f"No users with 'username={username} found in the database")
            return None

    async def change_user_banned_status_by_id(self, *, banned: bool, user_id: int, ) -> None:
        """Меняет статус бана пользователя по его id"""
        await self.session.execute(
            update(User).where(User.user_id == user_id).values(banned=banned)
        )
        await self.session.commit()
        logger.info(f"Updated 'banned' status to {banned} for user {user_id}")

    async def change_user_banned_status_by_username(
            self,
            *,
            banned: bool,
            username: str,
    ) -> None:
        """Меняет статус бана пользователя по его username"""
        await self.session.execute(
            update(User).where(User.username == username).values(banned=banned)
        )
        await self.session.commit()
        logger.info(f"Updated 'banned' status to {banned} for username {username}")

    async def write_user_name_phone_address(
            self,
            *,
            user_id: int,
            name: str,
            phone: int,
            address: str,
    ) -> None:
        """Вносит в БД имя, телефон и адрес пользователя"""
        await self.session.execute(
            update(User).where(User.user_id == user_id).values(name=name, phone=phone, address=address)
        )
        await self.session.commit()
        logger.info(f"Updated name {name}, phone {phone}, address {address} for user {user_id}")

    async def get_user_name_phone_address(self, *, user_id: int) -> list[dict]:
        """Проверяет, есть ли в БД имя, телефон и адрес пользователя"""
        result = await self.session.execute(
            select(User.name, User.phone, User.address)
            .where(User.user_id == user_id)
        )

        return [
            {"name": row[0], "phone": row[1], "address": row[2]}
            for row in result.all()
        ]

    async def get_users_list_for_broadcast(self):
        """Возвращает список пользователей для рассылки"""
        result = await self.session.execute(
            select(User.user_id)
            .where(User.is_alive == True, User.banned == False)
        )
        row = result.fetchall()
        return [user_telegram_id for (user_telegram_id,) in row]


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # === Категории ===
    async def get_all_categories(self) -> list[Category]:
        """Возвращает список всех категорий"""
        result = await self.session.execute(
            select(Category).where(Category.is_active == True)
        )
        return list(result.scalars().all())

    # === Товары ===
    async def get_products_by_category(self, category_id: int) -> list[Product]:
        """Возвращает список всех продуктов выбранной категории"""
        result = await self.session.execute(
            select(Product).
            where(Product.category_id == category_id, Product.is_available == True)
        )
        return list(result.scalars().all())

    async def get_product_by_id(self, product_id: int):
        """Возвращает продукт по его id"""
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()


class CartService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> CartItem:
        """Добавляет товар в корзину (или увеличивает количество, если товар уже есть)"""
        # Проверяем, есть ли уже такой товар в корзине
        result = await self.session.execute(
            select(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            )
        )
        item = result.scalar_one_or_none()

        if item:
            # Увеличиваем количество
            item.quantity += quantity
            await self.session.commit()
            return item
        else:
            # Создаем новый элемент
            new_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
            )
            self.session.add(new_item)
            await self.session.commit()
            return new_item

    async def get_cart_items(self, user_id: int) -> list[CartItem]:
        """Возвращает все товары в корзине пользователя"""
        result = await self.session.execute(
            select(CartItem)
            .where(CartItem.user_id == user_id)
            .order_by(CartItem.added_at)
        )
        return list(result.scalars().all())

    async def get_cart_items_with_info(self, user_id: int) -> list[dict]:
        """Возвращает все товары в корзине пользователя с подробной информацией"""
        result = await self.session.execute(
            select(Product.name, Product.id, CartItem.quantity, Product.price)
            .join(CartItem, Product.id == CartItem.product_id)
            .where(CartItem.user_id == user_id)
        )
        return [
            {"name": row[0], "id": row[1], "qnty": row[2], "price": row[3]}
            for row in result.all()
        ]

    async def remove_from_cart(self, user_id: int, product_id: int) -> None:
        """Уменьшает количество товара в корзине (или удаляет товар, если количество = 0)"""
        result = await self.session.execute(
            select(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id,
            )
        )
        item = result.scalar()
        # Уменьшаем позицию на одну
        item.quantity -= 1
        # Проверяем остаток, если равен 0, то удаляем товар из корзины
        if item.quantity == 0:
            await self.session.execute(
                delete(CartItem).
                where(CartItem.user_id == user_id,
                      CartItem.product_id == product_id
                      )
            )
        await self.session.commit()

    async def get_cart_total(self, user_id: int) -> int:
        """Возвращаем общую сумму корзины"""
        result = await self.session.execute(
            select(CartItem.quantity, Product.price)
            .join(Product, Product.id == CartItem.product_id)
            .where(CartItem.user_id == user_id)
        )
        total = sum(qty * price for qty, price in result.fetchall())
        return total

    async def clear_cart(self, user_id: int):
        """Очищает корзину пользователя"""
        await self.session.execute(
            delete(CartItem).where(CartItem.user_id == user_id)
        )
        await self.session.commit()
