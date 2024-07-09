from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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
    customer_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String)
    total_price = Column(Float)
    pizzas = relationship("OrderPizza", back_populates="order")

class OrderPizza(Base):
    __tablename__ = 'order_pizza'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    pizza_id = Column(Integer, ForeignKey('pizzas.id'))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="pizzas")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_delivery_partner = Column(Boolean, default=False)
