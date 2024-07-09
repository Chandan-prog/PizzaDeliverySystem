from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, models
from typing import List
from .auth import get_current_user 

router = APIRouter()

@router.get("/pizzas/", response_model=List[schemas.Pizza])
def read_pizzas(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    pizzas = crud.get_pizzas(db, skip=skip, limit=limit)
    return pizzas

@router.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_order(db, order, current_user.id)

@router.get("/orders/", response_model=List[schemas.Order])
def read_orders(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    orders = crud.get_orders(db, current_user.id)
    return orders
