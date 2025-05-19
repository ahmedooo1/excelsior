from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import MovingCreate, MovingResponse, MovingUpdate
from app.crud import get_moving, get_movings, get_moving_by_order, create_moving, update_moving, delete_moving
from app.database import get_db

router = APIRouter()

@router.post("/movings/", response_model=MovingResponse)
def create_new_moving(moving: MovingCreate, db: Session = Depends(get_db)):
    return create_moving(db=db, moving=moving)

@router.get("/movings/", response_model=List[MovingResponse])
def read_movings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movings = get_movings(db, skip=skip, limit=limit)
    return movings

@router.get("/movings/{moving_id}", response_model=MovingResponse)
def read_moving(moving_id: int, db: Session = Depends(get_db)):
    db_moving = get_moving(db, moving_id=moving_id)
    if db_moving is None:
        raise HTTPException(status_code=404, detail="Déménagement non trouvé")
    return db_moving

@router.get("/orders/{order_id}/moving", response_model=MovingResponse)
def read_order_moving(order_id: int, db: Session = Depends(get_db)):
    db_moving = get_moving_by_order(db, order_id=order_id)
    if db_moving is None:
        raise HTTPException(status_code=404, detail="Déménagement non trouvé pour cette commande")
    return db_moving

@router.patch("/movings/{moving_id}", response_model=MovingResponse)
def update_moving_info(moving_id: int, moving_data: MovingUpdate, db: Session = Depends(get_db)):
    db_moving = update_moving(db, moving_id=moving_id, moving_data=moving_data)
    if db_moving is None:
        raise HTTPException(status_code=404, detail="Déménagement non trouvé")
    return db_moving

@router.delete("/movings/{moving_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_moving_endpoint(moving_id: int, db: Session = Depends(get_db)):
    success = delete_moving(db, moving_id=moving_id)
    if not success:
        raise HTTPException(status_code=404, detail="Déménagement non trouvé")
    return {"detail": "Déménagement supprimé avec succès"}
