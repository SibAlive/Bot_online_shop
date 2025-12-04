from sqlalchemy import (Column, BigInteger, String, Boolean, DateTime,
                        func, Integer, Numeric, ForeignKey,)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from bot.enums import UserRole
from web import db


# Модель пользователя
class User(db.Model):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    language = Column(String(10), nullable=False)
    role = Column(ENUM(UserRole, name="user_role_enum"), nullable=False)
    is_alive = Column(Boolean, nullable=False)
    banned = Column(Boolean, nullable=False)
    name = Column(String(30), nullable=True)
    phone = Column(String(11), nullable=True)
    address = Column(String(50), nullable=True)

    # Связь с корзиной
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, user_id={self.user_id}, username='{self.username}')>"


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="cart_items")
    products = relationship("Product", back_populates="cart_items")

    def __repr__(self):
        return f"<CartItem(user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})>"


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связь с товарами
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"


class Product(db.Model):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)  # или Integer для копеек/тийинов
    photo_url = Column(String(500))  # URL фото (можно хранить file_id Telegram)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Связь с категорией
    category = relationship("Category", back_populates="products")
    # Связь с корзиной
    cart_items = relationship("CartItem", back_populates="products", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"