from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import TransportCreate, TransportResponse, TransportUpdate
from app.crud import get_transport, get_transports, get_transport_by_order, create_transport, update_transport, delete_transport
from app.database import get_db

router = APIRouter()

@router.post("/transports/", response_model=TransportResponse)
def create_new_transport(transport: TransportCreate, db: Session = Depends(get_db)):
    return create_transport(db=db, transport=transport)

@router.get("/transports/", response_model=List[TransportResponse])
def read_transports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transports = get_transports(db, skip=skip, limit=limit)
    return transports

@router.get("/transports/{transport_id}", response_model=TransportResponse)
def read_transport(transport_id: int, db: Session = Depends(get_db)):
    db_transport = get_transport(db, transport_id=transport_id)
    if db_transport is None:
        raise HTTPException(status_code=404, detail="Transport non trouvé")
    return db_transport

@router.get("/orders/{order_id}/transport", response_model=TransportResponse)
def read_order_transport(order_id: int, db: Session = Depends(get_db)):
    db_transport = get_transport_by_order(db, order_id=order_id)
    if db_transport is None:
        raise HTTPException(status_code=404, detail="Transport non trouvé pour cette commande")
    return db_transport

@router.patch("/transports/{transport_id}", response_model=TransportResponse)
def update_transport_info(transport_id: int, transport_data: TransportUpdate, db: Session = Depends(get_db)):
    db_transport = update_transport(db, transport_id=transport_id, transport_data=transport_data)
    if db_transport is None:
        raise HTTPException(status_code=404, detail="Transport non trouvé")
    return db_transport

@router.delete("/transports/{transport_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transport_endpoint(transport_id: int, db: Session = Depends(get_db)):
    success = delete_transport(db, transport_id=transport_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transport non trouvé")
    return {"detail": "Transport supprimé avec succès"}
