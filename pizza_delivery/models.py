from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Pizza(Base):
    __tablename__ = 'pizzas'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    is_available = Column(Boolean, default=True)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total = Column(Float)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    items = relationship("OrderItem", back_populates="order")
    delivery_partner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    delivery_partner = relationship("User", foreign_keys=[delivery_partner_id], back_populates="delivery_orders")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_delivery_partner = Column(Boolean, default=False)
    cart = relationship("Cart", back_populates="user", uselist=False)   #uselist tells one to one relationship
    orders = relationship("Order", back_populates="user", foreign_keys=[Order.user_id])
    delivery_orders = relationship("Order", back_populates="delivery_partner", foreign_keys=[Order.delivery_partner_id])



class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    total = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    pizza_id = Column(Integer, ForeignKey('pizzas.id'))
    quantity = Column(Integer, default=1)
    cart = relationship("Cart", back_populates="items")
    pizza = relationship("Pizza")


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    pizza_id = Column(Integer, ForeignKey('pizzas.id'))
    quantity = Column(Integer, default=1)
    order = relationship("Order", back_populates="items")
    pizza = relationship("Pizza")

User.cart = relationship("Cart", back_populates="user", uselist=False)
User.orders = relationship("Order", back_populates="user", foreign_keys=[Order.user_id])
User.delivery_orders = relationship("Order", back_populates="delivery_partner", foreign_keys=[Order.delivery_partner_id])

# These lines establish relationships on the User model after all the related models (Cart, Order) have been fully defined. 
# This is necessary because these relationships reference columns and models that may not be fully available until all models are declared.

# User.cart:

# Establishes a one-to-one relationship between User and Cart.
# uselist=False ensures that a user can have only one cart.
# User.orders:

# Establishes a one-to-many relationship between User and Order based on the user_id foreign key in Order.
# User.delivery_orders:

# Establishes a one-to-many relationship between User and Order based on the delivery_partner_id foreign key in Order.
# These relationships allow us to navigate from a User to their cart, orders, and delivery_orders, 
# enabling efficient querying and data manipulation within the system.