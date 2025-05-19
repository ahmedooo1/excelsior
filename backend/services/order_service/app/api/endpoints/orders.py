from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import OrderCreate, OrderResponse, OrderUpdate
from app.crud import get_order, get_orders, get_user_orders, create_order, update_order, delete_order
from app.database import get_db

router = APIRouter()

@router.post("/orders/", response_model=OrderResponse)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db=db, order=order)

@router.get("/orders/", response_model=List[OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = get_orders(db, skip=skip, limit=limit)
    return orders

@router.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return db_order

@router.get("/users/{user_id}/orders/", response_model=List[OrderResponse])
def read_user_orders(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = get_user_orders(db, user_id=user_id, skip=skip, limit=limit)
    return orders

@router.patch("/orders/{order_id}", response_model=OrderResponse)
def update_order_status(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    db_order = update_order(db, order_id=order_id, order_data=order_data)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return db_order

@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    success = delete_order(db, order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return {"detail": "Commande supprimée avec succès"}
