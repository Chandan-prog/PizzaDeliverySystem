from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, models
from .auth import get_current_delivery_partner

router = APIRouter()

@router.put("/orders/{order_id}/status", response_model=schemas.Order)
def update_order_status(order_id: int, status: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_delivery_partner)):
    db_order = crud.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

@router.put("/orders/{order_id}/comment", response_model=schemas.Order)
def add_order_comment(order_id: int, comment: str, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_delivery_partner)):
    db_order = crud.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.comment = comment
    db.commit()
    db.refresh(db_order)
    return db_order
