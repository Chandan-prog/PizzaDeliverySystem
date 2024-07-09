from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_pizza(db: Session, pizza_id: int):
    return db.query(models.Pizza).filter(models.Pizza.id == pizza_id).first()

def get_pizzas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Pizza).offset(skip).limit(limit).all()


def create_pizza(db: Session, pizza: schemas.PizzaCreate):
    db_pizza = models.Pizza(**pizza.model_dump())
    db.add(db_pizza)
    db.commit()
    db.refresh(db_pizza)
    return db_pizza

def update_pizza(db: Session, pizza: schemas.PizzaUpdate):
    db_pizza = db.query(models.Pizza).filter(models.Pizza.id == pizza.id).first()
    if db_pizza:
        for key, value in pizza.model_dump().items():
            setattr(db_pizza, key, value)
        db.commit()
        db.refresh(db_pizza)
    return db_pizza


def delete_pizza(db: Session, pizza_id: int):
    db_pizza = db.query(models.Pizza).filter(models.Pizza.id == pizza_id).first()
    if db_pizza:
        db.delete(db_pizza)
        db.commit()
    return db_pizza

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        is_admin=user.is_admin,
        is_delivery_partner=user.is_delivery_partner
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_order(db: Session, order: schemas.OrderCreate, customer_id: int):
    db_order = models.Order(
        customer_id=customer_id, status=order.status, total_price=order.total_price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for pizza in order.pizzas:
        order_pizza = models.OrderPizza(
            order_id=db_order.id, pizza_id=pizza.pizza_id, quantity=pizza.quantity
        )
        db.add(order_pizza)
    db.commit()
    return db_order

def get_orders(db: Session, customer_id: int):
    return db.query(models.Order).filter(models.Order.customer_id == customer_id).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()
