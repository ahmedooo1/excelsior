from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import ChildAssistanceCreate, ChildAssistanceResponse, ChildAssistanceUpdate
from app.crud import get_child_assistance, get_child_assistances, get_child_assistance_by_order, create_child_assistance, update_child_assistance, delete_child_assistance
from app.database import get_db

router = APIRouter()

@router.post("/child-assistances/", response_model=ChildAssistanceResponse)
def create_new_child_assistance(child_assistance: ChildAssistanceCreate, db: Session = Depends(get_db)):
    return create_child_assistance(db=db, child_assistance=child_assistance)

@router.get("/child-assistances/", response_model=List[ChildAssistanceResponse])
def read_child_assistances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    child_assistances = get_child_assistances(db, skip=skip, limit=limit)
    return child_assistances

@router.get("/child-assistances/{child_assistance_id}", response_model=ChildAssistanceResponse)
def read_child_assistance(child_assistance_id: int, db: Session = Depends(get_db)):
    db_child_assistance = get_child_assistance(db, child_assistance_id=child_assistance_id)
    if db_child_assistance is None:
        raise HTTPException(status_code=404, detail="Service de garde d'enfant non trouvé")
    return db_child_assistance

@router.get("/orders/{order_id}/child-assistance", response_model=ChildAssistanceResponse)
def read_order_child_assistance(order_id: int, db: Session = Depends(get_db)):
    db_child_assistance = get_child_assistance_by_order(db, order_id=order_id)
    if db_child_assistance is None:
        raise HTTPException(status_code=404, detail="Service de garde d'enfant non trouvé pour cette commande")
    return db_child_assistance

@router.patch("/child-assistances/{child_assistance_id}", response_model=ChildAssistanceResponse)
def update_child_assistance_info(child_assistance_id: int, child_assistance_data: ChildAssistanceUpdate, db: Session = Depends(get_db)):
    db_child_assistance = update_child_assistance(db, child_assistance_id=child_assistance_id, child_assistance_data=child_assistance_data)
    if db_child_assistance is None:
        raise HTTPException(status_code=404, detail="Service de garde d'enfant non trouvé")
    return db_child_assistance

@router.delete("/child-assistances/{child_assistance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_child_assistance_endpoint(child_assistance_id: int, db: Session = Depends(get_db)):
    success = delete_child_assistance(db, child_assistance_id=child_assistance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service de garde d'enfant non trouvé")
    return {"detail": "Service de garde d'enfant supprimé avec succès"}
