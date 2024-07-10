from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models, database
from .auth import get_current_user
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/cart", response_model=schemas.Cart)
def create_cart(user: schemas.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    db_cart = crud.get_cart(db, user.id)
    if db_cart:
        raise HTTPException(status_code=400, detail="User already has a cart")
    return crud.create_cart(db, schemas.CartCreate(user_id=user.id, total=0.0, is_active=True))

@router.post("/cart/items", response_model=schemas.CartItem)
def add_item_to_cart(item: schemas.CartItemCreate, user: schemas.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    db_cart = crud.get_cart(db, user.id)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return crud.add_item_to_cart(db, item, db_cart.id)

@router.get("/cart", response_model=schemas.Cart)
def read_cart(user: schemas.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    db_cart = crud.get_cart(db, user.id)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart



@router.post("/orders", response_model=schemas.Order)
def create_order( db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    db_cart = crud.get_cart(db, current_user.id)
    if not db_cart or not db_cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total based on items in the cart
    total = sum(item.quantity * item.pizza.price for item in db_cart.items)
    
    # Create OrderCreate object with all necessary fields
    order_create = schemas.OrderCreate(
        items=[schemas.OrderItemCreate(pizza_id=item.pizza_id, quantity=item.quantity) for item in db_cart.items],
        user_id=current_user.id,
        total=total,
        status="Pending",
        created_at=datetime.utcnow()  # Set current datetime for created_at
    )
    
    # Create order in database
    db_order = crud.create_order(db, order_create, current_user.id)
    
    # Create order items
    for item in order_create.items:
        crud.create_order_item(db, schemas.OrderItemCreate(order_id=db_order.id, **item.dict()))
    
    # Clear the cart
    db.query(models.CartItem).filter(models.CartItem.cart_id == db_cart.id).delete()
    db_cart.total = 0
    db.commit()
    db.refresh(db_cart)
    
    return db_order

@router.get("/orders", response_model=List[schemas.Order])
def read_orders(user: schemas.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    return crud.get_orders(db, user.id)

