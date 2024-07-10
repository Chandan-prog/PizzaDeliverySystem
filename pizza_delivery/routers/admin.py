from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models, database
from typing import List

router = APIRouter()

@router.post("/pizzas/", response_model=schemas.Pizza)
def create_pizza(pizza: schemas.PizzaCreate, db: Session = Depends(database.get_db)):
    return crud.create_pizza(db, pizza)

@router.get("/pizzas/{pizza_id}", response_model=schemas.Pizza)
def read_pizza(pizza_id: int, db: Session = Depends(database.get_db)):
    db_pizza = crud.get_pizza(db, pizza_id)
    if db_pizza is None:
        raise HTTPException(status_code=404, detail="Pizza not found")
    return db_pizza

@router.get("/pizzas", response_model=List[schemas.Pizza])
def read_pizzas(db: Session = Depends(database.get_db)):
    db_pizzas = crud.get_pizzas(db)
    return db_pizzas


@router.put("/pizzas/{pizza_id}", response_model=schemas.Pizza)
def update_pizza(pizza_id: int, pizza: schemas.Pizza, db: Session = Depends(database.get_db)):
    db_pizza = crud.update_pizza(db, pizza)
    if db_pizza is None:
        raise HTTPException(status_code=404, detail="Pizza not found")
    return db_pizza


@router.delete("/pizzas/{pizza_id}", response_model=schemas.Pizza)
def delete_pizza(pizza_id: int, db: Session = Depends(database.get_db)):
    db_pizza = crud.delete_pizza(db, pizza_id)
    if db_pizza is None:
        raise HTTPException(status_code=404, detail="Pizza not found")
    return db_pizza

