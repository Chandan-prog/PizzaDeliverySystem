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

def update_pizza(db: Session, pizza: schemas.Pizza):
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

def get_cart(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).first()

def create_cart(db: Session, cart: schemas.CartCreate):
    db_cart = models.Cart(**cart.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def add_item_to_cart(db: Session, cart_item: schemas.CartItemCreate, cart_id: int):
    db_cart_item = models.CartItem(**cart_item.dict(), cart_id=cart_id)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def get_orders(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()


def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    db_order = models.Order(user_id=user_id, total=order.total, status=order.status, delivery_partner_id=order.delivery_partner_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item in order.items:
        db_order_item = models.OrderItem(order_id=db_order.id, **item.dict())
        db.add(db_order_item)
        db.commit()
        db.refresh(db_order_item)
    
    return db_order

def create_order_item(db: Session, order_item: schemas.OrderItemCreate):
    db_order_item = models.OrderItem(**order_item.dict())
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

def get_all_orders(db: Session):
    return db.query(models.Order).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update_order_status(db: Session, order_id: int, status: str):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order