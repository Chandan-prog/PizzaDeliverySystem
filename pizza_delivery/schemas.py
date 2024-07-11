from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class PizzaBase(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool

class PizzaCreate(PizzaBase):
    pass

class Pizza(PizzaBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    is_admin: bool = False
    is_delivery_partner: bool = False

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_delivery_partner: bool

    class Config:
        orm_mode = True

class CartItemBase(BaseModel):
    pizza_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    pizza: Pizza

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    user_id: int
    total: float
    is_active: bool

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    items: List[CartItem]

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    pizza_id: int
    quantity: int

class OrderItemCreate(BaseModel):
    pizza_id: int
    quantity: int

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    user_id: int
    total: float
    status: str
    created_at: datetime
    delivery_partner_id: Optional[int]

    class Config:
        orm_mode = True

class OrderItem(OrderItemBase):
    id: int
    pizza: Pizza

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int
    total: float
    status: str
    created_at: datetime


class Order(OrderBase):
    id: int
    items: List[OrderItem]
    delivery_partner_id: Optional[int]

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
