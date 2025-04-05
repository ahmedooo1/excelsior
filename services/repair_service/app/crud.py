from sqlalchemy.orm import Session
from app.models import Repair
from app.schemas import RepairCreate, RepairUpdate

def get_repair(db: Session, repair_id: int):
    """Récupère un service de dépannage par son ID"""
    return db.query(Repair).filter(Repair.id == repair_id).first()

def get_repair_by_order(db: Session, order_id: int):
    """Récupère un service de dépannage par l'ID de la commande associée"""
    return db.query(Repair).filter(Repair.order_id == order_id).first()

def get_repairs(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste de services de dépannage avec pagination"""
    return db.query(Repair).offset(skip).limit(limit).all()

def create_repair(db: Session, repair: RepairCreate):
    """Crée un nouveau service de dépannage"""
    db_repair = Repair(
        order_id=repair.order_id,
        issue_type=repair.issue_type,
        technician_name=repair.technician_name,
        status="en route"
    )
    db.add(db_repair)
    db.commit()
    db.refresh(db_repair)
    return db_repair

def update_repair(db: Session, repair_id: int, repair_data: RepairUpdate):
    """Met à jour les informations d'un service de dépannage"""
    db_repair = get_repair(db, repair_id)
    if db_repair:
        update_data = repair_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_repair, key, value)
        db.commit()
        db.refresh(db_repair)
    return db_repair

def delete_repair(db: Session, repair_id: int):
    """Supprime un service de dépannage"""
    db_repair = get_repair(db, repair_id)
    if db_repair:
        db.delete(db_repair)
        db.commit()
        return True
    return False
