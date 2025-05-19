from sqlalchemy.orm import Session
from app.models import Cleaning
from app.schemas import CleaningCreate, CleaningUpdate

def get_cleaning(db: Session, cleaning_id: int):
    """Récupère un service de nettoyage par son ID"""
    return db.query(Cleaning).filter(Cleaning.id == cleaning_id).first()

def get_cleaning_by_order(db: Session, order_id: int):
    """Récupère un service de nettoyage par l'ID de la commande associée"""
    return db.query(Cleaning).filter(Cleaning.order_id == order_id).first()

def get_cleanings(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste de services de nettoyage avec pagination"""
    return db.query(Cleaning).offset(skip).limit(limit).all()

def create_cleaning(db: Session, cleaning: CleaningCreate):
    """Crée un nouveau service de nettoyage"""
    db_cleaning = Cleaning(
        order_id=cleaning.order_id,
        location_type=cleaning.location_type,
        cleaning_duration=cleaning.cleaning_duration,
        status="préparation"
    )
    db.add(db_cleaning)
    db.commit()
    db.refresh(db_cleaning)
    return db_cleaning

def update_cleaning(db: Session, cleaning_id: int, cleaning_data: CleaningUpdate):
    """Met à jour les informations d'un service de nettoyage"""
    db_cleaning = get_cleaning(db, cleaning_id)
    if db_cleaning:
        update_data = cleaning_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_cleaning, key, value)
        db.commit()
        db.refresh(db_cleaning)
    return db_cleaning

def delete_cleaning(db: Session, cleaning_id: int):
    """Supprime un service de nettoyage"""
    db_cleaning = get_cleaning(db, cleaning_id)
    if db_cleaning:
        db.delete(db_cleaning)
        db.commit()
        return True
    return False
