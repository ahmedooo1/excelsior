from sqlalchemy.orm import Session
from app.models import Moving
from app.schemas import MovingCreate, MovingUpdate

def get_moving(db: Session, moving_id: int):
    """Récupère un déménagement par son ID"""
    return db.query(Moving).filter(Moving.id == moving_id).first()

def get_moving_by_order(db: Session, order_id: int):
    """Récupère un déménagement par l'ID de la commande associée"""
    return db.query(Moving).filter(Moving.order_id == order_id).first()

def get_movings(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste de déménagements avec pagination"""
    return db.query(Moving).offset(skip).limit(limit).all()

def create_moving(db: Session, moving: MovingCreate):
    """Crée un nouveau déménagement"""
    db_moving = Moving(
        order_id=moving.order_id,
        team_size=moving.team_size,
        truck_size=moving.truck_size,
        status="préparation"
    )
    db.add(db_moving)
    db.commit()
    db.refresh(db_moving)
    return db_moving

def update_moving(db: Session, moving_id: int, moving_data: MovingUpdate):
    """Met à jour les informations d'un déménagement"""
    db_moving = get_moving(db, moving_id)
    if db_moving:
        update_data = moving_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_moving, key, value)
        db.commit()
        db.refresh(db_moving)
    return db_moving

def delete_moving(db: Session, moving_id: int):
    """Supprime un déménagement"""
    db_moving = get_moving(db, moving_id)
    if db_moving:
        db.delete(db_moving)
        db.commit()
        return True
    return False
