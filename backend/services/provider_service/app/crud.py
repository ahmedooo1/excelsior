from sqlalchemy.orm import Session
from app.models import Provider
from app.schemas import ProviderCreate, ProviderUpdate

def get_provider(db: Session, provider_id: int):
    """Récupère un prestataire par son ID"""
    return db.query(Provider).filter(Provider.id == provider_id).first()

def get_provider_by_email(db: Session, email: str):
    """Récupère un prestataire par son email"""
    return db.query(Provider).filter(Provider.email == email).first()

def get_providers(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste de prestataires avec pagination"""
    return db.query(Provider).offset(skip).limit(limit).all()

def get_available_providers(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste de prestataires disponibles"""
    return db.query(Provider).filter(Provider.availability == True).offset(skip).limit(limit).all()

def create_provider(db: Session, provider: ProviderCreate):
    """Crée un nouveau prestataire"""
    db_provider = Provider(
        name=provider.name,
        email=provider.email,
        latitude=provider.latitude,
        longitude=provider.longitude,
        availability=True
    )
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

def update_provider(db: Session, provider_id: int, provider_data: ProviderUpdate):
    """Met à jour les informations d'un prestataire"""
    db_provider = get_provider(db, provider_id)
    if db_provider:
        update_data = provider_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_provider, key, value)
        db.commit()
        db.refresh(db_provider)
    return db_provider

def delete_provider(db: Session, provider_id: int):
    """Supprime un prestataire"""
    db_provider = get_provider(db, provider_id)
    if db_provider:
        db.delete(db_provider)
        db.commit()
        return True
    return False
