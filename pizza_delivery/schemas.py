from pydantic import BaseModel
from typing import List, Optional

class PizzaBase(BaseModel):
    name: str
    description: str
    price: float
    is_available: bool

class PizzaCreate(PizzaBase):
    pass

class PizzaUpdate(PizzaBase):
    id: int

class Pizza(PizzaBase):
    id: int

    class Config:
        orm_mode = True

class OrderPizza(BaseModel):
    pizza_id: int
    quantity: int

class OrderBase(BaseModel):
    status: str
    total_price: float
    pizzas: List[OrderPizza]

class OrderCreate(OrderBase):
    customer_id: int

class OrderUpdate(OrderBase):
    id: int

class Order(OrderBase):
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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
