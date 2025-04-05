from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import CleaningCreate, CleaningResponse, CleaningUpdate
from app.crud import get_cleaning, get_cleanings, get_cleaning_by_order, create_cleaning, update_cleaning, delete_cleaning
from app.database import get_db

router = APIRouter()

@router.post("/cleanings/", response_model=CleaningResponse)
def create_new_cleaning(cleaning: CleaningCreate, db: Session = Depends(get_db)):
    return create_cleaning(db=db, cleaning=cleaning)

@router.get("/cleanings/", response_model=List[CleaningResponse])
def read_cleanings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cleanings = get_cleanings(db, skip=skip, limit=limit)
    return cleanings

@router.get("/cleanings/{cleaning_id}", response_model=CleaningResponse)
def read_cleaning(cleaning_id: int, db: Session = Depends(get_db)):
    db_cleaning = get_cleaning(db, cleaning_id=cleaning_id)
    if db_cleaning is None:
        raise HTTPException(status_code=404, detail="Service de nettoyage non trouvé")
    return db_cleaning

@router.get("/orders/{order_id}/cleaning", response_model=CleaningResponse)
def read_order_cleaning(order_id: int, db: Session = Depends(get_db)):
    db_cleaning = get_cleaning_by_order(db, order_id=order_id)
    if db_cleaning is None:
        raise HTTPException(status_code=404, detail="Service de nettoyage non trouvé pour cette commande")
    return db_cleaning

@router.patch("/cleanings/{cleaning_id}", response_model=CleaningResponse)
def update_cleaning_info(cleaning_id: int, cleaning_data: CleaningUpdate, db: Session = Depends(get_db)):
    db_cleaning = update_cleaning(db, cleaning_id=cleaning_id, cleaning_data=cleaning_data)
    if db_cleaning is None:
        raise HTTPException(status_code=404, detail="Service de nettoyage non trouvé")
    return db_cleaning

@router.delete("/cleanings/{cleaning_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cleaning_endpoint(cleaning_id: int, db: Session = Depends(get_db)):
    success = delete_cleaning(db, cleaning_id=cleaning_id)
    if not success:
        raise HTTPException(status_code=404, detail="Service de nettoyage non trouvé")
    return {"detail": "Service de nettoyage supprimé avec succès"}
