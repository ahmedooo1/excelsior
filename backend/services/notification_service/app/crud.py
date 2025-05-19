from sqlalchemy.orm import Session
from app.models import Notification
from app.schemas import NotificationCreate, NotificationUpdate

def get_notification(db: Session, notification_id: int):
    """Récupère une notification par son ID"""
    return db.query(Notification).filter(Notification.id == notification_id).first()

def get_notifications(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste de notifications avec pagination"""
    return db.query(Notification).offset(skip).limit(limit).all()

def get_user_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Récupère les notifications d'un utilisateur spécifique"""
    return db.query(Notification).filter(Notification.user_id == user_id).offset(skip).limit(limit).all()

def create_notification(db: Session, notification: NotificationCreate):
    """Crée une nouvelle notification"""
    db_notification = Notification(
        user_id=notification.user_id,
        message=notification.message,
        is_read=False
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def update_notification(db: Session, notification_id: int, notification_data: NotificationUpdate):
    """Met à jour le statut de lecture d'une notification"""
    db_notification = get_notification(db, notification_id)
    if db_notification:
        update_data = notification_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_notification, key, value)
        db.commit()
        db.refresh(db_notification)
    return db_notification

def delete_notification(db: Session, notification_id: int):
    """Supprime une notification"""
    db_notification = get_notification(db, notification_id)
    if db_notification:
        db.delete(db_notification)
        db.commit()
        return True
    return False
