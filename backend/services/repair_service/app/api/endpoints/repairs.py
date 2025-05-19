from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import RepairCreate, RepairResponse, RepairUpdate
from app.crud import get_repair, get_repairs, get_repair_by_order, create_repair, update_repair, delete_repair
from app.database import get_db

router = APIRouter()

@router.post("/repairs/", response_model=RepairResponse)
def create_new_repair(repair: RepairCreate, db: Session = Depends(get_db)):
    return create_repair(db=db, repair=repair)

@router.get("/repairs/", response_model=List[RepairResponse])
def read_repairs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repairs = get_repairs(db, skip=skip, limit=limit)
    return repairs

@router.get("/repairs/{repair_id}", response_model=RepairResponse)
def read_repair(repair_id: int, db: Session = Depends(get_db)):
    db_repair = get_repair(db, repair_id=repair_id)
    if db_repair is None:
        raise HTTPException(status_code=404, detail="Service de dépannage non trouvé")
    return db_repair

@router.get("/orders/{order_id}/repair", response_model=RepairResponse)
def read_order_repair(order_id: int, db: Session = Depends(get_db)):
    db_repair = get_repair_by_order(db, order_id=order_id)
    if db_repair is None:
        raise HTTPException(status_code=404, detail="Service de dépannage non trouvé pour cette commande")
    return db_repair

@router.patch("/repairs/{repair_id}", response_model=RepairResponse)
def update_repair_info(repair_id: int, repair_data: RepairUpdate, db: Session = Depends(get_db)):
    db_repair = update_repair(db, repair_id=repair_id, repair_data=repair_data)
    if db_repair is None:
        raise HTTPException(status_code=404, detail="Service de dépannage non trouvé")
    return db_repair

@router.delete("/repairs/{repair_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repair_endpoint(repair_id: int, db: Session = Depends(get_db)):
    success = delete_repair(db, repair_id=repair_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service de dépannage non trouvé")
    return {"detail": "Service de dépannage supprimé avec succès"}
