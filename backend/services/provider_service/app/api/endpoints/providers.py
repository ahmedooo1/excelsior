from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import ProviderCreate, ProviderResponse, ProviderUpdate
from app.crud import get_provider, get_providers, get_available_providers, get_provider_by_email, create_provider, update_provider, delete_provider
from app.database import get_db

router = APIRouter()

@router.post("/providers/", response_model=ProviderResponse)
def create_new_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    db_provider = get_provider_by_email(db, email=provider.email)
    if db_provider:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return create_provider(db=db, provider=provider)

@router.get("/providers/", response_model=List[ProviderResponse])
def read_providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    providers = get_providers(db, skip=skip, limit=limit)
    return providers

@router.get("/providers/available/", response_model=List[ProviderResponse])
def read_available_providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    providers = get_available_providers(db, skip=skip, limit=limit)
    return providers

@router.get("/providers/{provider_id}", response_model=ProviderResponse)
def read_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = get_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Prestataire non trouvé")
    return db_provider

@router.patch("/providers/{provider_id}", response_model=ProviderResponse)
def update_provider_info(provider_id: int, provider_data: ProviderUpdate, db: Session = Depends(get_db)):
    db_provider = update_provider(db, provider_id=provider_id, provider_data=provider_data)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Prestataire non trouvé")
    return db_provider

@router.delete("/providers/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_provider_endpoint(provider_id: int, db: Session = Depends(get_db)):
    success = delete_provider(db, provider_id=provider_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prestataire non trouvé")
    return {"detail": "Prestataire supprimé avec succès"}
