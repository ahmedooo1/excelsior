from sqlalchemy.orm import Session
from app.models import ChildAssistance
from app.schemas import ChildAssistanceCreate, ChildAssistanceUpdate

def get_child_assistance(db: Session, child_assistance_id: int):
    """Récupère un service de garde d'enfant par son ID"""
    return db.query(ChildAssistance).filter(ChildAssistance.id == child_assistance_id).first()

def get_child_assistance_by_order(db: Session, order_id: int):
    """Récupère un service de garde d'enfant par l'ID de la commande associée"""
    return db.query(ChildAssistance).filter(ChildAssistance.order_id == order_id).first()

def get_child_assistances(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste de services de garde d'enfant avec pagination"""
    return db.query(ChildAssistance).offset(skip).limit(limit).all()

def create_child_assistance(db: Session, child_assistance: ChildAssistanceCreate):
    """Crée un nouveau service de garde d'enfant"""
    db_child_assistance = ChildAssistance(
        order_id=child_assistance.order_id,
        guardian_name=child_assistance.guardian_name,
        child_count=child_assistance.child_count,
        destination=child_assistance.destination,
        status="en cours"
    )
    db.add(db_child_assistance)
    db.commit()
    db.refresh(db_child_assistance)
    return db_child_assistance

def update_child_assistance(db: Session, child_assistance_id: int, child_assistance_data: ChildAssistanceUpdate):
    """Met à jour les informations d'un service de garde d'enfant"""
    db_child_assistance = get_child_assistance(db, child_assistance_id)
    if db_child_assistance:
        update_data = child_assistance_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_child_assistance, key, value)
        db.commit()
        db.refresh(db_child_assistance)
    return db_child_assistance

def delete_child_assistance(db: Session, child_assistance_id: int):
    """Supprime un service de garde d'enfant"""
    db_child_assistance = get_child_assistance(db, child_assistance_id)
    if db_child_assistance:
        db.delete(db_child_assistance)
        db.commit()
        return True
    return False
